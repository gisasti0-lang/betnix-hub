"""
Corre los tres ciclos (C1, C2, C3) contra la MISMA entrada real y emite tres
registros que validan contra entrega2/corridas/esquema.json.

Diseño del experimento:
  - Telegram se lee UNA sola vez. Los tres ciclos consumen ese mismo snapshot,
    así `hash_entrada` es idéntico por construcción y no por suerte.
  - Ningún ciclo envía mensajes (`envios_reales` = 0 en los tres). Suprimir el
    efecto saliente es el control del experimento, no un atajo: lo que se compara
    es qué PUBLICA cada contrato, y eso se computa sin escribirle a nadie.
  - Lo único que varía entre C2 y C3 es la versión del contrato.

Uso:
    source .env && python3 correr_ciclos.py
"""

import asyncio
import hashlib
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import openpyxl
from telethon import TelegramClient
from telethon.tl.types import User

from anonimizar import categoria, franja, seudonimo

BASE       = Path(__file__).parent
RUNS_DIR   = BASE / "corridas"
EXCEL_PATH = "/Users/fernandoisasti/Documents/Betnix Partners/Betnix_Outreach_2026.xlsx"
HOURS_BACK = 24

API_ID   = os.environ.get("BETNIX_TG_API_ID")
API_HASH = os.environ.get("BETNIX_TG_API_HASH")

PROMPT_ITER2 = (
    "El script funciona bien. Ahora quiero agregar dos cosas: 1) que actualice "
    "el Excel con Ultimo contacto y Ultimo mensaje; 2) que suba un resumen JSON "
    "a GitHub Pages. Repo: gisasti0-lang/betnix-hub, archivo: resumen.json"
)
PROMPT_ITER1 = (
    "Tengo un Excel con ~211 contactos de Telegram. Quiero que todas las mananas "
    "un script lea los handles, revise mensajes de las ultimas 24h, responda "
    "automaticamente y me deje un resumen en consola."
)


def h16(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:16]


async def leer_snapshot() -> dict:
    """Una sola lectura de la realidad. Los tres ciclos la comparten."""
    wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True)
    ws = wb.active
    handles = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        contacto, canal = str(row[1] or "").strip(), str(row[2] or "").strip()
        if canal == "Telegram" and contacto.startswith("@"):
            handles.add(contacto.lstrip("@").lower())
    wb.close()

    client = TelegramClient(str(BASE / "betnix_session"), int(API_ID), API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        sys.exit("✗ Sesión no válida. Corré login.py con las credenciales nuevas.")

    cutoff, vistos, activos = (
        datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK), 0, []
    )
    async for dialog in client.iter_dialogs():
        e = dialog.entity
        if not isinstance(e, User):
            continue
        vistos += 1
        u = (e.username or "").lower()
        if u not in handles:
            continue
        entrantes = []
        async for m in client.iter_messages(e, limit=20):
            if m.date < cutoff:
                break
            if not m.out:
                entrantes.append(m)
        if entrantes:
            activos.append({
                "handle": u,
                "nombre": f"{e.first_name or ''} {e.last_name or ''}".strip(),
                "texto":  entrantes[0].text or "",
                "fecha":  entrantes[0].date,
                "n":      len(entrantes),
            })
    await client.disconnect()

    return {"handles": handles, "vistos": vistos, "activos": activos}


# ── Cómo publica cada contrato ────────────────────────────────────────────────
def payload_c1(snap):   # v1: sólo consola, no publica nada
    return None

def payload_c2(snap):   # v2: publica handle, nombre y texto  <-- el problema
    return {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "chats_activos": len(snap["activos"]),
        "contactos_excel": len(snap["handles"]),
        "resumen": [
            {"handle": f"@{a['handle']}", "nombre": a["nombre"],
             "fecha": a["fecha"].strftime("%d/%m %H:%M"), "mensaje": a["texto"][:120]}
            for a in snap["activos"]
        ],
    }

def payload_c3(snap):   # v3: agregado + seudonimizado
    por_cat = {}
    for a in snap["activos"]:
        c = categoria(a["texto"])
        por_cat[c] = por_cat.get(c, 0) + 1
    return {
        "esquema": "betnix-hub/resumen@2",
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "chats_activos": len(snap["activos"]),
        "contactos_excel": len(snap["handles"]),
        "por_categoria": por_cat,
        "actividad": [
            {"id": seudonimo(a["handle"]), "franja": franja(a["fecha"]),
             "categoria": categoria(a["texto"]), "mensajes": a["n"]}
            for a in snap["activos"]
        ],
    }


def redactar(obj):
    """Conserva la FORMA del payload y borra los valores.

    El registro de C2 tiene que probar que ese contrato publicaba handle,
    nombre y texto — pero sin publicarlos. Se reemplaza cada valor por un
    marcador de tipo: la evidencia queda, el dato personal no.
    """
    if isinstance(obj, dict):
        return {k: redactar(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redactar(o) for o in obj[:1]] + (
            [f"<... {len(obj) - 1} entradas más omitidas>"] if len(obj) > 1 else []
        )
    if isinstance(obj, bool) or isinstance(obj, int):
        return obj
    return f"<{type(obj).__name__} redactado>"


CICLOS = [
    {"ciclo": "C1", "version": "v1", "pieza": None,
     "prompt": PROMPT_ITER1, "prompt_id": "iteracion_1",
     "destinos": ["consola"], "campos": [],
     "campos_pii": [], "creds": 2, "payload": payload_c1,
     "check": dict(flujo_numerado=True, manejo_errores=False,
                   secretos_fuera_del_codigo=False, advierte_riesgo_tos=True,
                   salida_persistente=False, sin_pii_publicada=True)},

    {"ciclo": "C2", "version": "v2", "pieza": "P5",
     "prompt": PROMPT_ITER2, "prompt_id": "iteracion_2",
     "destinos": ["consola", "excel", "github_pages"],
     "campos": ["handle", "nombre", "fecha", "mensaje"],
     "campos_pii": ["handle", "nombre", "mensaje"], "creds": 3, "payload": payload_c2,
     "check": dict(flujo_numerado=True, manejo_errores=True,
                   secretos_fuera_del_codigo=False, advierte_riesgo_tos=True,
                   salida_persistente=True, sin_pii_publicada=False)},

    {"ciclo": "C3", "version": "v3", "pieza": "P2.regla3",
     "prompt": PROMPT_ITER2, "prompt_id": "iteracion_2",   # MISMO caso que C2
     "destinos": ["consola", "excel", "github_pages"],
     "campos": ["id", "franja", "categoria", "mensajes"],
     "campos_pii": [], "creds": 0, "payload": payload_c3,
     "check": dict(flujo_numerado=True, manejo_errores=True,
                   secretos_fuera_del_codigo=True, advierte_riesgo_tos=True,
                   salida_persistente=True, sin_pii_publicada=True)},
]


async def main():
    if not API_ID or not API_HASH:
        sys.exit("✗ Falta BETNIX_TG_API_ID / BETNIX_TG_API_HASH. Ver .env.example")

    print("Leyendo Telegram una sola vez (sin enviar nada)...")
    snap = await leer_snapshot()
    print(f"  contactos en Excel: {len(snap['handles'])}")
    print(f"  diálogos vistos:    {snap['vistos']}")
    print(f"  chats con actividad: {len(snap['activos'])}\n")

    # Identidad de la entrada: idéntica para los tres por construcción
    hash_entrada = h16("|".join(sorted(a["handle"] for a in snap["activos"]))
                       + f"#{len(snap['handles'])}#{HOURS_BACK}")

    RUNS_DIR.mkdir(exist_ok=True)
    ahora = datetime.now()

    for c in CICLOS:
        reg = {
            "corrida_id":   f"{c['ciclo']}_{ahora:%Y%m%d_%H%M%S}",
            "ciclo":        c["ciclo"],
            "ejecutado_en": ahora.isoformat(timespec="seconds"),
            "contrato": {"version": c["version"], "pieza_modificada": c["pieza"],
                         "piezas_totales": 5},
            "caso": {"prompt_id": c["prompt_id"], "hash_prompt": h16(c["prompt"])},
            "entrada": {"contactos_excel": len(snap["handles"]),
                        "ventana_horas": HOURS_BACK,
                        "dialogos_vistos": snap["vistos"],
                        "hash_entrada": hash_entrada},
            "salida": {"chats_activos": len(snap["activos"]),
                       "destinos": c["destinos"],
                       "campos_publicados": c["campos"],
                       "envios_reales": 0},
            "privacidad": {"pii_en_payload": bool(c["campos_pii"]),
                           "campos_pii": c["campos_pii"],
                           "credenciales_en_codigo": c["creds"]},
            "checklist": c["check"],
        }
        p = c["payload"](snap)

        # Copia local completa: evidencia cruda, nunca se commitea (.gitignore)
        if p is not None:
            local = dict(reg, payload_publicable=p)
            (RUNS_DIR / f"_local_corrida_{c['ciclo'].lower()}.json").write_text(
                json.dumps(local, ensure_ascii=False, indent=2, default=str))
            # C3 ya es seudonimizado por diseño: se publica tal cual.
            reg["payload_publicable"] = p if not c["campos_pii"] else redactar(p)

        destino = RUNS_DIR / f"corrida_{c['ciclo'].lower()}.json"
        destino.write_text(json.dumps(reg, ensure_ascii=False, indent=2, default=str))
        print(f"  ✓ {destino.name}  — contrato {c['version']}, "
              f"pieza modificada: {c['pieza'] or '(línea base)'}")

    print(f"\nMismo hash_entrada en las tres: {hash_entrada}")
    print("Ninguna corrida envió mensajes.")
    print("\ncorrida_c2.json va REDACTADO (forma sí, valores no).")
    print("La evidencia cruda queda en _local_corrida_*.json, fuera de git.")


if __name__ == "__main__":
    asyncio.run(main())
