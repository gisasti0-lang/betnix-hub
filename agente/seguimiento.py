"""
Agente de seguimiento de prospección — Betnix.

Lee un lote de prospectos seudonimizados del pipeline, decide a cuáles
corresponde seguimiento y redacta el mensaje. NO envía nada: escribe la salida a
disco y termina. El envío depende de la aprobación humana, que ocurre fuera de
este proceso (ver GOBIERNO.md, nivel de autonomía L2).

    python3 agente/seguimiento.py --entrada corridas/2026-09-09/entrada.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal

import anthropic
from pydantic import BaseModel, Field

RAIZ = Path(__file__).resolve().parent.parent
SYSTEM_PROMPT = RAIZ / "prompts" / "system_prompt.md"

# El modelo es una constante de configuración, no una decisión enterrada en el
# código. La comparación contra alternativas está en ANALISIS_ECONOMICO.md.
MODELO = "claude-opus-5"
MAX_TOKENS = 8000

# Tarifas USD por millón de tokens. Se declaran acá para que el cálculo de
# costo sea recalculable a mano desde el registro de la corrida.
TARIFAS = {
    "claude-opus-5":  {"entrada": 5.00, "salida": 25.00},
    "claude-sonnet-5": {"entrada": 3.00, "salida": 15.00},
    "claude-haiku-4-5": {"entrada": 1.00, "salida": 5.00},
}

class Resultado(BaseModel):
    id: str = Field(description="Seudónimo del prospecto, formato PR-xxxxxxxx")
    corresponde: bool = Field(description="si le toca seguimiento hoy")
    prioridad: Literal["alta", "media", "baja", "ninguna"]
    motivo: str = Field(description="clave del criterio aplicado, pocas palabras")
    requiere_decision: bool = Field(
        description="true si toca dinero, tarifas o negociación pendiente")
    mensaje: str = Field(description="Hasta 500 caracteres, o cadena vacía")
    nota: str = Field(description="Observación del agente, una línea")


class Resumen(BaseModel):
    corresponden: int
    requieren_decision: int
    por_prioridad: dict[str, int]


class SalidaSeguimiento(BaseModel):
    fecha_lote: str
    procesados: int
    resultados: list[Resultado]
    resumen: Resumen


def cargar_system_prompt() -> str:
    """Extrae el contrato de prompts/system_prompt.md.

    El archivo es el entregable: se lee de ahí y no se duplica en el código,
    para que no puedan divergir.
    """
    if not SYSTEM_PROMPT.is_file():
        sys.exit(f"✗ Falta {SYSTEM_PROMPT}")
    return SYSTEM_PROMPT.read_text()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True, help="JSON del lote de mensajes")
    ap.add_argument("--salida", help="dónde escribir; por defecto junto a la entrada")
    args = ap.parse_args()

    ruta_entrada = Path(args.entrada)
    if not ruta_entrada.is_file():
        sys.exit(f"✗ No existe {ruta_entrada}")
    lote = json.loads(ruta_entrada.read_text())

    if not lote.get("prospectos"):
        sys.exit("✗ El lote no tiene prospectos.")

    client = anthropic.Anthropic()
    inicio = datetime.now()

    try:
        respuesta = client.messages.parse(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            system=cargar_system_prompt(),
            messages=[{"role": "user", "content": json.dumps(lote, ensure_ascii=False)}],
            output_format=SalidaSeguimiento,
        )
    except anthropic.RateLimitError as e:
        sys.exit(f"✗ Límite de tasa alcanzado: {e}")
    except anthropic.APIStatusError as e:
        sys.exit(f"✗ Error de la API ({e.status_code}): {e}")
    except anthropic.APIConnectionError as e:
        sys.exit(f"✗ No se pudo conectar: {e}")

    salida: SalidaSeguimiento = respuesta.parsed_output
    uso = respuesta.usage
    tarifa = TARIFAS[MODELO]
    costo = (uso.input_tokens / 1e6 * tarifa["entrada"]
             + uso.output_tokens / 1e6 * tarifa["salida"])

    destino = Path(args.salida) if args.salida else ruta_entrada.parent / "salida.json"
    destino.write_text(json.dumps(salida.model_dump(), ensure_ascii=False, indent=2))

    meta = {
        "fecha": inicio.isoformat(timespec="seconds"),
        "modelo": MODELO,
        "max_tokens": MAX_TOKENS,
        "tokens_entrada": uso.input_tokens,
        "tokens_salida": uso.output_tokens,
        "tarifa_usd_por_millon": tarifa,
        "costo_usd": round(costo, 6),
        "duracion_seg": round((datetime.now() - inicio).total_seconds(), 1),
        "prospectos_en_lote": len(lote["prospectos"]),
        "enviados": 0,
        "nota": "Ningún mensaje fue enviado. El envío requiere aprobación humana.",
    }
    (destino.parent / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2))

    print(f"\n  Procesados:          {salida.procesados}")
    print(f"  Corresponde seguir:  {salida.resumen.corresponden}")
    print(f"  Requieren decisión:  {salida.resumen.requieren_decision}")
    print(f"  Tokens E/S:          {uso.input_tokens} / {uso.output_tokens}")
    print(f"  Costo de la corrida: USD {costo:.6f}")
    print(f"  Salida:              {destino}")
    print(f"\n  ⏸  Nada fue enviado. Revisá los mensajes antes de aprobar.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
