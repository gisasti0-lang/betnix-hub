"""
Construye el lote de entrada del agente a partir del pipeline de prospección.

Este es el único punto donde el nombre de la empresa y el contacto existen en
memoria. Salen de acá seudonimizados: el prompt del agente nunca ve una razón
social, un @handle ni un email.

    python3 agente/construir_lote.py --salida corridas/2026-09-09/entrada.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import openpyxl

from anonimizar import seudonimo

EXCEL = Path.home() / "Documents" / "Betnix Partners" / "Betnix_Outreach_2026.xlsx"

# Columnas de la planilla, por índice (0-based).
COL = {"empresa": 0, "contacto": 1, "canal": 2, "campana": 3,
       "geo": 4, "trafico": 5, "estado": 6, "cierre": 7, "comentario": 8}

# La planilla usa vocabulario de outreach; el contrato del agente declara un
# enum cerrado. El mapeo vive acá y no en el prompt.
ESTADO_CRM = {
    "already working": "activo",
    "launching": "en_alta",
    "contacted": "prospecto",
    "sin respuesta": "sin_respuesta",
    "not replying": "sin_respuesta",
    "not relevant": "descartado",
    "rebotó": "descartado",
    "reboto": "descartado",
    "no se pudo cerrar": "descartado",
}

# Criterio de selección: determinista y declarado, para que el lote sea
# reproducible. Quién entra al lote lo decide el código; qué se le dice a cada
# uno lo decide el agente.
ESTADOS_ELEGIBLES = {"activo", "en_alta", "prospecto", "sin_respuesta"}
CIERRES_EXCLUIDOS = {"rojo"}

# Orden de atención. Un lote diario de 217 no es un lote diario: nadie hace 217
# seguimientos en un día, y el prompt no entraría. Se ordena por probabilidad de
# cierre y se corta. El orden es determinista, así que el lote es reproducible.
ORDEN_CIERRE = {"verde": 0, "amarillo": 1, "—": 2}
TOPE_DIARIO = 25


def limpio(v) -> str:
    return " ".join(str(v or "").split()).strip()


def construir(limite: int | None, desde: int) -> dict:
    if not EXCEL.is_file():
        sys.exit(f"✗ No se encuentra la planilla: {EXCEL}")

    wb = openpyxl.load_workbook(EXCEL, read_only=True)
    filas = [f for f in wb.active.iter_rows(values_only=True) if any(f)]
    wb.close()

    prospectos, descartados, sin_contacto = [], 0, 0

    for fila in filas[1:]:
        contacto = limpio(fila[COL["contacto"]])
        if not contacto or contacto == "—":
            sin_contacto += 1
            continue

        estado = ESTADO_CRM.get(limpio(fila[COL["estado"]]).lower(), "desconocido")
        cierre = limpio(fila[COL["cierre"]]) or "—"

        if estado not in ESTADOS_ELEGIBLES or cierre.lower() in CIERRES_EXCLUIDOS:
            descartados += 1
            continue

        prospectos.append({
            # La razón social y el contacto mueren acá. El seudónimo se deriva
            # del contacto, que es el identificador único de la fila.
            "id": seudonimo(contacto),
            "canal": limpio(fila[COL["canal"]]) or "—",
            "geo": limpio(fila[COL["geo"]]) or "—",
            "tipo_trafico": limpio(fila[COL["trafico"]]) or "—",
            "estado": estado,
            "posibilidad_cierre": cierre,
            "campana": limpio(fila[COL["campana"]]) or "—",
            "comentario": limpio(fila[COL["comentario"]])[:300],
        })

    prospectos.sort(key=lambda p: (
        ORDEN_CIERRE.get(p["posibilidad_cierre"].lower(), 3),
        p["id"],                       # desempate estable
    ))
    total_elegibles = len(prospectos)
    tope = limite or TOPE_DIARIO
    prospectos = prospectos[desde:desde + tope]

    print(f"Filas con datos:       {len(filas) - 1}")
    print(f"Sin contacto usable:   {sin_contacto}")
    print(f"Fuera de criterio:     {descartados}")
    print(f"Elegibles:             {total_elegibles}")
    print(f"En el lote:            {len(prospectos)}  (desde el #{desde + 1})")

    return {"fecha_lote": datetime.now().strftime("%Y-%m-%d"),
            "prospectos": prospectos}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--limite", type=int,
                    help=f"tamaño del lote; por defecto {TOPE_DIARIO}")
    ap.add_argument("--desde", type=int, default=0,
                    help="desplazamiento en la lista ordenada; el lote diario avanza")
    args = ap.parse_args()

    lote = construir(args.limite, args.desde)
    if not lote["prospectos"]:
        sys.exit("✗ Lote vacío: ninguna fila cumple el criterio de selección.")

    destino = Path(args.salida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(lote, ensure_ascii=False, indent=2))
    print(f"Escrito: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
