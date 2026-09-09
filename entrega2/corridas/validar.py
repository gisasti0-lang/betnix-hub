"""
Valida que las tres corridas cumplan el esquema único y que el experimento
esté realmente aislado. Sin dependencias externas.

    python3 validar.py
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent


def check(cond, ok, err):
    print(("  ✓ " if cond else "  ✗ ") + (ok if cond else err))
    return cond


def validar_contra_esquema(reg, esquema):
    """Chequeo estructural mínimo: required, enums, const y additionalProperties."""
    fallas = []

    def rec(obj, esq, ruta=""):
        for k in esq.get("required", []):
            if k not in obj:
                fallas.append(f"{ruta}{k}: faltante")
        props = esq.get("properties", {})
        if esq.get("additionalProperties") is False:
            for k in obj:
                if k not in props:
                    fallas.append(f"{ruta}{k}: no permitido")
        for k, v in obj.items():
            sub = props.get(k)
            if not sub:
                continue
            if "enum" in sub and v not in sub["enum"]:
                fallas.append(f"{ruta}{k}: '{v}' fuera de {sub['enum']}")
            if "const" in sub and v != sub["const"]:
                fallas.append(f"{ruta}{k}: {v!r} != {sub['const']!r}")
            if sub.get("type") == "object" and isinstance(v, dict):
                rec(v, sub, f"{ruta}{k}.")

    rec(reg, esquema)
    return fallas


def main():
    esquema = json.loads((BASE / "esquema.json").read_text())
    archivos = sorted(BASE.glob("corrida_c*.json"))

    if len(archivos) != 3:
        print(f"✗ Se esperaban 3 corridas, hay {len(archivos)}.")
        print("  Generalas con: source .env && python3 correr_ciclos.py")
        return 1

    regs = {}
    print("Validación estructural contra esquema.json")
    ok = True
    for f in archivos:
        r = json.loads(f.read_text())
        regs[r["ciclo"]] = r
        fallas = validar_contra_esquema(r, esquema)
        ok &= check(not fallas, f"{f.name}", f"{f.name}: {'; '.join(fallas)}")

    print("\nAislamiento del experimento")
    hashes = {c: r["entrada"]["hash_entrada"] for c, r in regs.items()}
    ok &= check(len(set(hashes.values())) == 1,
                "las tres corridas comparten la misma entrada real",
                f"entradas distintas: {hashes}")

    ok &= check(regs["C2"]["caso"]["hash_prompt"] == regs["C3"]["caso"]["hash_prompt"],
                "C2 y C3 corren el MISMO caso (mismo prompt)",
                "C3 no repite el caso de C2 — el ciclo no está aislado")

    piezas = {c: r["contrato"]["pieza_modificada"] for c, r in regs.items()}
    ok &= check(piezas["C3"] and piezas["C3"] != piezas["C2"],
                f"C3 modifica una pieza distinta a C2 ({piezas['C2']} → {piezas['C3']})",
                f"piezas mal declaradas: {piezas}")

    ok &= check(all(r["salida"]["envios_reales"] == 0 for r in regs.values()),
                "ninguna corrida envió mensajes",
                "alguna corrida envió mensajes reales")

    print("\nCorrección de privacidad")
    ok &= check(regs["C2"]["privacidad"]["pii_en_payload"] is True,
                "C2 publica PII (es el problema que se documenta)",
                "C2 debería exhibir el problema")
    ok &= check(regs["C3"]["privacidad"]["pii_en_payload"] is False,
                "C3 no publica PII",
                "C3 sigue publicando PII — la corrección no tomó efecto")
    ok &= check(regs["C3"]["privacidad"]["credenciales_en_codigo"] == 0,
                "C3 no tiene credenciales en el código",
                "C3 todavía tiene credenciales hardcodeadas")

    print("\n" + ("✓ TODO OK" if ok else "✗ HAY FALLAS"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
