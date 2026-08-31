# Salida 1 — Iteración 1: Script básico de resumen matutino

**Prompt usado:** Iteración 1 del `user_prompt.md`  
**Técnica:** RAG (el agente leyó el Excel como contexto) + Structured output (código Python listo para correr)

---

## Output del agente

**Flujo diseñado:**
1. Cargar handles de Telegram desde el Excel (col B, filtrar por col C = "Telegram")
2. Conectar con Telethon usando sesión preexistente (no pedir teléfono en cada corrida)
3. Iterar diálogos → filtrar usuarios → filtrar por handles del Excel
4. Revisar mensajes de las últimas 24h → identificar los entrantes (no enviados por mí)
5. Responder "Gracias, ya te respondo 🙌" solo una vez por día por contacto
6. Imprimir resumen en consola

```python
"""
Betnix Telegram Morning Summary — v1
"""
import asyncio, json, os
from datetime import datetime, timedelta, timezone
from pathlib import Path
import openpyxl
from telethon import TelegramClient
from telethon.tl.types import User

API_ID   = 32468859
API_HASH = "d72f0777926f3a22735bf2b9b765ddcb"
SESSION  = str(Path(__file__).parent / "betnix_session")
EXCEL    = "/Users/.../Betnix_Outreach_2026.xlsx"
LOG_PATH = str(Path(__file__).parent / "morning_log.json")

def load_handles(path):
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.active
    handles = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        if str(row[2] or "").strip() == "Telegram" and str(row[1] or "").startswith("@"):
            handles.add(str(row[1]).lstrip("@").lower())
    wb.close()
    return handles

async def main():
    handles = load_handles(EXCEL)
    cutoff  = datetime.now(timezone.utc) - timedelta(hours=24)
    log     = json.load(open(LOG_PATH)) if os.path.exists(LOG_PATH) else {}
    today   = datetime.now().strftime("%Y-%m-%d")

    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()

    async for dialog in client.iter_dialogs():
        if not isinstance(dialog.entity, User): continue
        username = (dialog.entity.username or "").lower()
        if username not in handles: continue

        msgs = [m async for m in client.iter_messages(dialog.entity, limit=20)
                if m.date >= cutoff and not m.out]
        if not msgs: continue

        ultimo = msgs[0]
        print(f"📩 @{username}: {(ultimo.text or '')[:80]}")

        key = f"{today}_{username}"
        if key not in log:
            await client.send_message(dialog.entity, "Gracias, ya te respondo 🙌")
            log[key] = True
            print(f"   ✅ Respondido")

    json.dump(log, open(LOG_PATH, "w"), indent=2)
    await client.disconnect()

asyncio.run(main())
```

**Instrucción de ejecución:**
```bash
python3 /Users/.../betnix-tg-morning/morning_summary.py
```

---

## Qué faltó en esta iteración

- No actualiza el Excel con la fecha del último mensaje
- No publica nada en la web → el resumen solo vive en consola
- Si la computadora está apagada a las 8 AM, no corre (no hay cron configurado)
