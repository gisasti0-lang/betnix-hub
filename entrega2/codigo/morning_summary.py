"""
Betnix Telegram Morning Summary — v3

Cambio único respecto de v2: el contrato de publicación prohíbe PII.
El resumen público pasa a ser agregado + seudonimizado; handle, nombre y texto
del mensaje se quedan en el Excel local y nunca viajan a GitHub Pages.

Credenciales por variable de entorno (ver .env.example). Nada hardcodeado.

Uso:
    python3 morning_summary.py --dry-run   # lee y reporta, no responde ni publica
    python3 morning_summary.py             # corrida real completa
"""

import argparse
import asyncio
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import openpyxl
from telethon import TelegramClient
from telethon.tl.types import User

from anonimizar import categoria, franja, seudonimo

# ── Config ────────────────────────────────────────────────────────────────────
BASE = Path(__file__).parent

API_ID   = os.environ.get("BETNIX_TG_API_ID")
API_HASH = os.environ.get("BETNIX_TG_API_HASH")
GH_TOKEN = os.environ.get("BETNIX_GH_TOKEN")

SESSION = str(BASE / "betnix_session")

GH_OWNER = "gisasti0-lang"
GH_REPO  = "betnix-hub"
GH_FILE  = "resumen.json"

EXCEL_PATH = "/Users/fernandoisasti/Documents/Betnix Partners/Betnix_Outreach_2026.xlsx"
LOG_PATH   = BASE / "morning_log.json"
RUNS_DIR   = BASE / "corridas"

AUTO_REPLY = "Gracias, ya te respondo 🙌"
HOURS_BACK = 24

CONTRATO_VERSION = "v3"  # queda registrado en cada corrida


# ── Excel ─────────────────────────────────────────────────────────────────────
def load_tg_handles_from_excel(path: str) -> set[str]:
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.active
    handles = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        contacto = str(row[1] or "").strip()   # col B
        canal    = str(row[2] or "").strip()   # col C
        if canal == "Telegram" and contacto.startswith("@"):
            handles.add(contacto.lstrip("@").lower())
    wb.close()
    return handles


def update_excel_last_contact(path: str, handle: str, mensaje: str, fecha: str):
    """El texto completo vive acá, en local. Nunca se publica."""
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    if ws.cell(1, 11).value != "Último contacto":
        ws.cell(1, 11).value = "Último contacto"
    if ws.cell(1, 12).value != "Último mensaje":
        ws.cell(1, 12).value = "Último mensaje"

    objetivo = handle.lower().lstrip("@")
    for row in ws.iter_rows(min_row=2):
        if str(row[1].value or "").strip().lstrip("@").lower() == objetivo:
            row[10].value = fecha
            row[11].value = mensaje[:200]
            break
    wb.save(path)
    wb.close()


def load_log() -> dict:
    return json.loads(LOG_PATH.read_text()) if LOG_PATH.exists() else {}


def save_log(log: dict):
    LOG_PATH.write_text(json.dumps(log, indent=2, ensure_ascii=False))


# ── Publicación ───────────────────────────────────────────────────────────────
def push_to_github(data: dict):
    if not GH_TOKEN:
        print("  ⚠️  BETNIX_GH_TOKEN no seteado — se omite la publicación")
        return "omitido_sin_token"

    api_url = f"https://api.github.com/repos/{GH_OWNER}/{GH_REPO}/contents/{GH_FILE}"
    headers = {
        "Authorization": f"token {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            sha = json.loads(resp.read()).get("sha", "")
    except urllib.error.HTTPError:
        sha = ""

    content = base64.b64encode(
        json.dumps(data, ensure_ascii=False, indent=2).encode()
    ).decode()
    payload = json.dumps({
        "message": f"update resumen {data.get('fecha', '')}",
        "content": content,
        **({"sha": sha} if sha else {}),
    }).encode()

    req = urllib.request.Request(api_url, data=payload, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"  🌐 GitHub Pages actualizado (HTTP {resp.getcode()})")
            return "ok"
    except urllib.error.HTTPError as e:
        print(f"  ⚠️  Error al publicar: {e}")
        return f"error_{e.code}"


# ── Main ──────────────────────────────────────────────────────────────────────
async def main(dry_run: bool):
    modo = "DRY-RUN (sin responder ni publicar)" if dry_run else "REAL"
    inicio = datetime.now()
    print(f"\n{'='*58}")
    print(f"  BETNIX MORNING SUMMARY {CONTRATO_VERSION} — {inicio:%d/%m/%Y %H:%M} — {modo}")
    print(f"{'='*58}\n")

    if not API_ID or not API_HASH:
        sys.exit("✗ Falta BETNIX_TG_API_ID / BETNIX_TG_API_HASH en el entorno.")

    handles_excel = load_tg_handles_from_excel(EXCEL_PATH)
    print(f"Contactos Telegram en Excel: {len(handles_excel)}")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)
    log    = load_log()
    today  = datetime.now().strftime("%Y-%m-%d")

    client = TelegramClient(SESSION, int(API_ID), API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        sys.exit("✗ Sesión no válida. Corré login.py primero.")

    publicable, respondidos, dialogos_vistos = [], 0, 0

    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if not isinstance(entity, User):
            continue
        dialogos_vistos += 1

        username = (entity.username or "").lower()
        if username not in handles_excel:
            continue

        entrantes = []
        async for msg in client.iter_messages(entity, limit=20):
            if msg.date < cutoff:
                break
            if not msg.out:
                entrantes.append(msg)
        if not entrantes:
            continue

        ultimo = entrantes[0]
        texto  = ultimo.text or ""

        # ── Lo único que se publica ───────────────────────────────────────────
        publicable.append({
            "id":        seudonimo(username),
            "franja":    franja(ultimo.date),
            "categoria": categoria(texto),
            "mensajes":  len(entrantes),
        })
        print(f"  📩 {seudonimo(username)} · {franja(ultimo.date)} · {categoria(texto)} · {len(entrantes)} msj")

        clave = f"{today}_{username}"
        if clave not in log:
            if dry_run:
                print("     ⏸  dry-run: no se envió la respuesta")
            else:
                await client.send_message(entity, AUTO_REPLY)
                log[clave] = {"franja": franja(ultimo.date), "categoria": categoria(texto)}
                respondidos += 1
                print("     ✅ Respondido")
        else:
            print("     ⏭  Ya respondido hoy")

        if not dry_run:
            update_excel_last_contact(EXCEL_PATH, username, texto,
                                      datetime.now().strftime("%d/%m/%Y %H:%M"))

    if not dry_run:
        save_log(log)

    # ── Payload público: agregados + seudónimos, cero PII ─────────────────────
    por_categoria = {}
    for r in publicable:
        por_categoria[r["categoria"]] = por_categoria.get(r["categoria"], 0) + 1

    gh_data = {
        "esquema":         "betnix-hub/resumen@2",
        "fecha":           today,
        "timestamp":       datetime.now().isoformat(timespec="seconds"),
        "contactos_excel": len(handles_excel),
        "chats_activos":   len(publicable),
        "respondidos":     respondidos,
        "por_categoria":   por_categoria,
        "actividad":       publicable,
    }

    estado_push = "omitido_dry_run" if dry_run else push_to_github(gh_data)
    await client.disconnect()

    # ── Registro de la corrida (esquema único de comparación) ─────────────────
    RUNS_DIR.mkdir(exist_ok=True)
    registro = {
        "corrida_id":        f"{today}_{inicio:%H%M%S}_{CONTRATO_VERSION}",
        "contrato_version":  CONTRATO_VERSION,
        "modo":              "dry_run" if dry_run else "real",
        "inicio":            inicio.isoformat(timespec="seconds"),
        "duracion_seg":      round((datetime.now() - inicio).total_seconds(), 1),
        "entrada": {
            "excel":            Path(EXCEL_PATH).name,
            "contactos_excel":  len(handles_excel),
            "ventana_horas":    HOURS_BACK,
            "dialogos_vistos":  dialogos_vistos,
        },
        "salida": {
            "chats_activos":  len(publicable),
            "respondidos":    respondidos,
            "excel_escrito":  not dry_run,
            "push_estado":    estado_push,
        },
        "privacidad": {
            "pii_en_payload":       False,
            "campos_publicados":    ["id", "franja", "categoria", "mensajes"],
            "campos_retenidos_local": ["handle", "nombre", "texto_mensaje"],
        },
        "payload_publicado": gh_data,
    }
    destino = RUNS_DIR / f"{registro['corrida_id']}.json"
    destino.write_text(json.dumps(registro, ensure_ascii=False, indent=2))

    print(f"\n{'─'*58}")
    print(f"  Chats con movimiento: {len(publicable)}")
    print(f"  Respuestas enviadas:  {respondidos}")
    print(f"  Registro de corrida:  {destino.name}")
    print(f"{'─'*58}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="lee y reporta, pero no responde ni publica")
    args = ap.parse_args()
    asyncio.run(main(args.dry_run))
