#!/bin/zsh
# Instala el agente de launchd y saca la entrada de cron que nunca funcionó.
set -u
DIR="/Users/fernandoisasti/betnix-tg-morning"
LABEL="com.betnix.morning"
DEST="$HOME/Library/LaunchAgents/$LABEL.plist"

echo "1) Sacando la entrada vieja de cron..."
if crontab -l 2>/dev/null | grep -q "morning_summary.py"; then
  crontab -l 2>/dev/null | grep -v "morning_summary.py" | crontab -
  echo "   ✓ entrada de cron eliminada (nunca llegó a ejecutarse)"
else
  echo "   · no había entrada de cron"
fi

echo "2) Instalando el agente..."
mkdir -p "$HOME/Library/LaunchAgents"
cp "$DIR/$LABEL.plist" "$DEST"
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null
launchctl bootstrap "gui/$(id -u)" "$DEST" 2>/dev/null
if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  echo "   ✓ agente cargado: $LABEL"
else
  echo "   ✗ no se pudo cargar. Revisá: launchctl print gui/$(id -u)/$LABEL"
  exit 1
fi

echo "3) Próximo disparo: mañana 08:00 (o al despertar la Mac)."
echo "   Para probarlo YA:  launchctl kickstart -k gui/$(id -u)/$LABEL"
echo "   Para ver el log:   tail -f $DIR/morning_log.txt"
