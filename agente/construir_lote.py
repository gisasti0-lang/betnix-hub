"""
Construye el lote de entrada del agente a partir de Telegram y el Excel.

Este es el único punto donde el handle real existe en memoria. Sale de acá
seudonimizado: el prompt del agente nunca ve un @handle, un nombre ni un teléfono.

    python3 agente/construir_lote.py --salida corridas/2026-09-09/entrada.json
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import openpyxl
from telethon import TelegramClient
from telethon.tl.types import User

from anonimizar import seudonimo

RAIZ = Path(__file__).resolve().parent.parent
SESION = str(Path.home() / "betnix-tg-morning" / "betnix_session")
EXCEL = str(Path.home() / "Documents" / "Betnix Partners" / "Betnix_Outreach_2026.xlsx")

API_ID = os.environ.get("BETNIX_TG_API_ID")
API_HASH = os.environ.get("BETNIX_TG_API_HASH")

HORAS = 24


def handles_y_estado() -> dict[str, str]:
    """Handle en minúscula -> estado del CRM, desde la columna F del Excel."""
    wb = openpyxl.load_workbook(EXCEL, read_only=True)
    ws = wb.active
    fuera = {}
    for fila in ws.iter_rows(min_row=2, values_only=True):
        contacto = str(fila[1] or "").strip()
        canal = str(fila[2] or "").strip()
        estado = str(fila[5] or "").strip().lower()
        if canal == "Telegram" and contacto.startswith("@"):
            fuera[contacto.lstrip("@").lower()] = (
                estado if estado in {"activo", "en_alta", "pausado"} else "desconocido"
            )
    wb.close()
    return fuera


async def main(destino: Path) -> int:
    if not API_ID or not API_HASH:
        sys.exit("✗ Falta BETNIX_TG_API_ID / BETNIX_TG_API_HASH en el entorno.")

    contactos = handles_y_estado()
    print(f"Contactos Telegram en el Excel: {len(contactos)}")

    corte = datetime.now(timezone.utc) - timedelta(hours=HORAS)
    client = TelegramClient(SESION, int(API_ID), API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        sys.exit("✗ Sesión no válida. Corré login.py primero.")

    mensajes = []
    async for dialogo in client.iter_dialogs():
        entidad = dialogo.entity
        if not isinstance(entidad, User):
            continue
        usuario = (entidad.username or "").lower()
        if usuario not in contactos:
            continue

        entrantes = []
        async for m in client.iter_messages(entidad, limit=20):
            if m.date < corte:
                break
            if not m.out:
                entrantes.append(m)
        if not entrantes:
            continue

        mensajes.append({
            "id": seudonimo(usuario),          # el handle muere acá
            "texto": entrantes[0].text or "",
            "mensajes_en_ventana": len(entrantes),
            "estado_crm": contactos[usuario],
        })

    await client.disconnect()

    lote = {"fecha_lote": datetime.now().strftime("%Y-%m-%d"), "mensajes": mensajes}
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(lote, ensure_ascii=False, indent=2))

    print(f"Mensajes en el lote: {len(mensajes)}")
    print(f"Escrito: {destino}")
    if not mensajes:
        print("⚠  Lote vacío: nadie escribió en las últimas 24 h.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()
    sys.exit(asyncio.run(main(Path(a.salida))))
