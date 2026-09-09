"""
Seudonimización estable para el hub público de Betnix.

Regla de oro: el handle, el nombre y el texto del mensaje NUNCA salen de esta
máquina. Lo único publicable es un seudónimo derivado con HMAC y una sal local
que no se versiona.

Sin la sal, el seudónimo no es reversible ni por fuerza bruta sobre el espacio
de handles conocidos.
"""
import hashlib
import hmac
import os
import re
import secrets
from pathlib import Path

SALT_PATH = Path(__file__).parent / ".salt"


def _get_salt() -> bytes:
    """Lee la sal local; la genera en la primera corrida. Nunca se publica."""
    if SALT_PATH.exists():
        return SALT_PATH.read_bytes()
    salt = secrets.token_bytes(32)
    SALT_PATH.write_bytes(salt)
    SALT_PATH.chmod(0o600)
    return salt


def seudonimo(handle: str) -> str:
    """@juan_perez -> AF-3f9a2c11. Estable entre corridas, no reversible."""
    h = handle.strip().lstrip("@").lower()
    digest = hmac.new(_get_salt(), h.encode(), hashlib.sha256).hexdigest()
    return f"AF-{digest[:8]}"


# ── Categorización del mensaje ────────────────────────────────────────────────
# Publicamos la categoría, nunca el texto. Determinista y sin LLM, para que la
# corrida sea reproducible byte a byte.
_CATEGORIAS = [
    ("pago",      r"\b(pago|pagos|cobro|comisi[oó]n|factura|transfer|retiro|ngr)\b"),
    ("deal",      r"\b(deal|cpa|revshare|rev\s?share|h[ií]brido|porcentaje|tarifa)\b"),
    ("soporte",   r"\b(error|problema|no\s+funciona|link|postback|tracker|ayuda)\b"),
    ("alta",      r"\b(alta|registro|registrar|sumarme|empezar|arrancar|onboarding)\b"),
    ("saludo",    r"\b(hola|buenas|buen d[ií]a|gracias|ok|dale|listo)\b"),
]


def categoria(texto: str) -> str:
    """Clasifica el mensaje en un enum fijo. El texto original no se publica."""
    if not texto:
        return "sin_texto"
    t = texto.lower()
    for nombre, patron in _CATEGORIAS:
        if re.search(patron, t):
            return nombre
    return "otro"


def franja(dt) -> str:
    """Hora redondeada a franja de 6h: evita reconstruir la actividad de nadie."""
    h = dt.hour
    if h < 6:
        return "00-06"
    if h < 12:
        return "06-12"
    if h < 18:
        return "12-18"
    return "18-24"
