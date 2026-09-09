#!/bin/zsh
# Verifica cada precondición para que la automatización corra de verdad.
DIR="/Users/fernandoisasti/betnix-tg-morning"
PY="/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
LABEL="com.betnix.morning"
ok=0; fail=0
chk() { if eval "$2" >/dev/null 2>&1; then echo "  ✓ $1"; ((ok++)); else echo "  ✗ $1"; ((fail++)); fi }

echo "Entorno"
chk "intérprete con telethon+openpyxl" "$PY -c 'import telethon,openpyxl'"
chk ".env existe"                      "[[ -f $DIR/.env ]]"
chk ".env sin placeholders"            "! grep -q '<nuevo_' $DIR/.env"
chk ".env con permisos 600"            "[[ \$(stat -f %Lp $DIR/.env) == 600 ]]"
chk "sal de seudonimización"           "[[ -f $DIR/.salt ]]"

echo "Datos"
chk "Excel accesible"  "[[ -r '/Users/fernandoisasti/Documents/Betnix Partners/Betnix_Outreach_2026.xlsx' ]]"
chk "sesión de Telegram" "[[ -f $DIR/betnix_session.session ]]"

echo "Automatización"
chk "wrapper ejecutable"     "[[ -x $DIR/run_morning.sh ]]"
chk "plist instalado"        "[[ -f $HOME/Library/LaunchAgents/$LABEL.plist ]]"
chk "agente cargado"         "launchctl print gui/\$(id -u)/$LABEL"
chk "cron viejo eliminado"   "! crontab -l 2>/dev/null | grep -q morning_summary"

echo "Seguridad"
chk "sin secretos en el código" "! grep -rqE 'ghp_[A-Za-z0-9]{20,}|d72f0777' $DIR/*.py"
chk ".env ignorado por git"     "grep -q '^.env$' $DIR/.gitignore"

echo
echo "  $ok OK · $fail pendientes"
[[ $fail -eq 0 ]] && echo "  Todo listo." || echo "  Resolvé los ✗ antes de confiar en el disparo de las 08:00."
