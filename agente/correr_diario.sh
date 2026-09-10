#!/bin/zsh
# Pipeline diario del agente de seguimiento, disparado por launchd a las 08:00.
#
# Hace exactamente lo que declara GOBIERNO.md: lee la planilla, arma el lote
# seudonimizado, el agente decide y redacta, y TERMINA. No envía nada.
set -u
REPO="/Users/fernandoisasti/betnix-hub"
ENV_FILE="/Users/fernandoisasti/betnix-tg-morning/.env"
PY="/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
LOG="$REPO/agente/diario.log"
FECHA="$(date +%F)"
DEST="$REPO/corridas/$FECHA"

exec >> "$LOG" 2>&1
echo "───────────────────────────────────────────────"
echo "▶ $(date '+%Y-%m-%d %H:%M:%S')  inicio"

[[ -f "$ENV_FILE" ]] || { echo "✗ falta $ENV_FILE"; exit 1; }
source "$ENV_FILE"

if [[ -z "${ANTHROPIC_API_KEY:-}" || "$ANTHROPIC_API_KEY" == "<"* ]]; then
  echo "✗ ANTHROPIC_API_KEY sin completar. El agente no puede correr."
  exit 1
fi

cd "$REPO/agente" || exit 1

echo "· construyendo el lote"
"$PY" construir_lote.py --salida "$DEST/entrada.json" || {
  echo "✗ falló la construcción del lote"; exit 1; }

echo "· corriendo el agente"
"$PY" seguimiento.py --entrada "$DEST/entrada.json" || {
  echo "✗ falló el agente"; exit 1; }

echo "◀ $(date '+%H:%M:%S')  fin — nada enviado, revisar $DEST/salida.json"
