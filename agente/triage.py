"""
Agente de triage de mensajes de afiliados — Betnix.

Lee un lote de mensajes entrantes seudonimizados, los clasifica y redacta un
borrador de respuesta por cada uno. NO envía nada: escribe la salida a disco y
termina. El envío depende de la aprobación humana, que ocurre fuera de este
proceso (ver GOBIERNO.md, nivel de autonomía L2).

    python3 agente/triage.py --entrada corridas/2026-09-09/entrada.json
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

Categoria = Literal["pago", "deal", "soporte", "alta", "saludo",
                    "manipulacion", "sin_contenido", "otro"]


class Resultado(BaseModel):
    id: str = Field(description="Seudónimo del afiliado, formato AF-xxxxxxxx")
    categoria: Categoria
    urgencia: Literal["alta", "media", "baja"]
    requiere_decision: bool = Field(
        description="true si el mensaje toca dinero, tarifas o plazos")
    borrador: str = Field(description="Hasta 400 caracteres, o cadena vacía")
    nota_triage: str = Field(description="Por qué se clasificó así, una línea")


class Resumen(BaseModel):
    requieren_decision: int
    por_categoria: dict[str, int]


class SalidaTriage(BaseModel):
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

    if not lote.get("mensajes"):
        sys.exit("✗ El lote no tiene mensajes.")

    client = anthropic.Anthropic()
    inicio = datetime.now()

    try:
        respuesta = client.messages.parse(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            system=cargar_system_prompt(),
            messages=[{"role": "user", "content": json.dumps(lote, ensure_ascii=False)}],
            output_format=SalidaTriage,
        )
    except anthropic.RateLimitError as e:
        sys.exit(f"✗ Límite de tasa alcanzado: {e}")
    except anthropic.APIStatusError as e:
        sys.exit(f"✗ Error de la API ({e.status_code}): {e}")
    except anthropic.APIConnectionError as e:
        sys.exit(f"✗ No se pudo conectar: {e}")

    salida: SalidaTriage = respuesta.parsed_output
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
        "mensajes_en_lote": len(lote["mensajes"]),
        "enviados": 0,
        "nota": "Ninguna respuesta fue enviada. El envío requiere aprobación humana.",
    }
    (destino.parent / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2))

    print(f"\n  Procesados:          {salida.procesados}")
    print(f"  Requieren decisión:  {salida.resumen.requieren_decision}")
    print(f"  Tokens E/S:          {uso.input_tokens} / {uso.output_tokens}")
    print(f"  Costo de la corrida: USD {costo:.6f}")
    print(f"  Salida:              {destino}")
    print(f"\n  ⏸  Nada fue enviado. Revisá los borradores antes de aprobar.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
