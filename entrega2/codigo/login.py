"""
Login único de Telegram. Después morning_summary.py reusa la sesión.
Requiere BETNIX_TG_API_ID / BETNIX_TG_API_HASH en el entorno (ver .env.example).
"""
import asyncio
import os
import sys
from pathlib import Path

from telethon import TelegramClient

API_ID   = os.environ.get("BETNIX_TG_API_ID")
API_HASH = os.environ.get("BETNIX_TG_API_HASH")
PHONE    = os.environ.get("BETNIX_TG_PHONE")
SESSION  = str(Path(__file__).parent / "betnix_session")


async def main():
    if not API_ID or not API_HASH:
        sys.exit("✗ Falta BETNIX_TG_API_ID / BETNIX_TG_API_HASH. Ver .env.example")

    client = TelegramClient(SESSION, int(API_ID), API_HASH)
    await client.start(phone=PHONE or input("Teléfono (+54...): "))
    me = await client.get_me()
    print(f"\n✅ Login OK como @{me.username}")
    await client.disconnect()


asyncio.run(main())
