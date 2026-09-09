#!/bin/zsh
# Wrapper para launchd: carga el entorno y corre el resumen matutino.
# launchd no hereda tu shell, así que las variables se cargan acá.
set -u
DIR="/Users/fernandoisasti/betnix-tg-morning"
PY="/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
LOG="$DIR/morning_log.txt"

cd "$DIR" || exit 1

echo "───────────────────────────────────────────────" >> "$LOG"
echo "▶ $(date '+%Y-%m-%d %H:%M:%S')  inicio" >> "$LOG"

if [[ ! -f "$DIR/.env" ]]; then
  echo "✗ falta .env — ver .env.example" >> "$LOG"
  exit 1
fi
source "$DIR/.env"

# El .env puede existir pero seguir con los placeholders del ejemplo.
# Sin este chequeo, el fallo aparece como un stack trace de int() a las 8 AM.
for VAR in BETNIX_TG_API_ID BETNIX_TG_API_HASH; do
  VAL="${(P)VAR:-}"
  if [[ -z "$VAL" || "$VAL" == "<"* ]]; then
    echo "✗ $VAR sin completar en .env — el agente no puede correr." >> "$LOG"
    echo "  Completalo con las credenciales de my.telegram.org y reintentá con:" >> "$LOG"
    echo "  launchctl kickstart -k gui/$(id -u)/com.betnix.morning" >> "$LOG"
    exit 1
  fi
done

if [[ ! -x "$PY" ]]; then
  echo "✗ intérprete no encontrado: $PY" >> "$LOG"
  exit 1
fi

"$PY" "$DIR/morning_summary.py" >> "$LOG" 2>&1
CODE=$?
echo "◀ $(date '+%H:%M:%S')  fin (exit $CODE)" >> "$LOG"
exit $CODE
