"""
Verifica cada afirmación de trazabilidad.json contra el repositorio.

El punto de este script es que las afirmaciones de la entrega no se crean:
se comprueban. Si una falla, la entrega está afirmando algo que no sostiene.

    python3 entrega2/evaluacion/verificar.py
"""
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent          # entrega2/


def leer(rel: str) -> str | None:
    p = (RAIZ / rel).resolve()
    return p.read_text(errors="replace") if p.is_file() else None


def evaluar(a: dict) -> tuple[bool, str]:
    tipo, patron, arch = a["chequeo"], a["patron"], a["archivo"]

    if tipo == "cuenta_glob":
        d = (RAIZ / arch).resolve()
        n = len(list(d.glob(patron))) if d.is_dir() else 0
        esperado = a.get("esperado", 0)
        return n == esperado, f"{n} archivo(s), esperado {esperado}"

    if tipo == "ausente_en_dir":
        d = (RAIZ / arch).resolve()
        if not d.is_dir():
            return False, f"no existe el directorio {arch}"
        rx = re.compile(patron)
        hits = [f.name for f in d.rglob("*")
                if f.is_file() and rx.search(f.read_text(errors="replace"))]
        return not hits, ("sin coincidencias" if not hits else f"aparece en {hits}")

    texto = leer(arch)
    if texto is None:
        return False, f"no existe el archivo {arch}"

    if tipo == "contiene":
        return patron in texto, ("encontrado" if patron in texto else "NO encontrado")

    if tipo == "no_contiene":
        m = re.search(patron, texto)
        return not m, ("ausente" if not m else f"aparece: {m.group(0)!r}")

    if tipo == "json_tiene":
        d = json.loads(texto)
        for k in patron.split("."):
            if not isinstance(d, dict) or k not in d:
                return False, f"falta la clave {patron}"
            d = d[k]
        return True, "clave presente"

    return False, f"tipo de chequeo desconocido: {tipo}"


def main() -> int:
    datos = json.loads((AQUI / "trazabilidad.json").read_text())
    afirmaciones = datos["afirmaciones"]

    ok = fallan = 0
    por_criterio: dict[int, list[bool]] = {}

    for a in afirmaciones:
        paso, detalle = evaluar(a)
        por_criterio.setdefault(a["criterio"], []).append(paso)
        marca = "✓" if paso else "✗"
        print(f"  {marca} {a['id']:<4} {a['afirmacion']}")
        if not paso:
            print(f"       └─ {a['archivo']}: {detalle}")
        ok, fallan = (ok + paso, fallan + (not paso))

    print(f"\n  {ok}/{len(afirmaciones)} afirmaciones verificadas")
    if fallan:
        print(f"  ✗ {fallan} sin sostén: la entrega afirma algo que el repo no respalda.")
        return 1
    print("  ✓ Toda afirmación central mapea a un artefacto que la sostiene.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
