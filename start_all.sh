#!/usr/bin/env bash
set -euo pipefail

# Pfade anpassen, falls nötig
ROOT="/home/zvs-admin/ZVS/ZVS"
VENV_PY="$ROOT/venv/bin/python"

cd "$ROOT"

# MySQL aus XAMPP starten (nur wenn nicht schon läuft)
if ! mysqladmin ping -h127.0.0.1 --silent >/dev/null 2>&1; then
  sudo /opt/lampp/lampp startmysql
fi

# Python-Binary ermitteln
if [[ -x "$VENV_PY" ]]; then
  PYTHON="$VENV_PY"
else
  PYTHON="$(command -v python3)"
fi

# App-Host/Port setzen (sofern von app.py ausgewertet)
export APP_HOST="0.0.0.0"
export APP_PORT="5000"

# Flask-App starten
"$PYTHON" app.py &
APP_PID=$!

# ngrok-Binary finden
NGROK_BIN="$(command -v ngrok || true)"
if [[ -z "$NGROK_BIN" ]]; then
  echo "ngrok nicht gefunden (PATH prüfen)."
  kill "$APP_PID"
  exit 1
fi

# ngrok starten
"$NGROK_BIN" http --url=zvs.ngrok.app 5000 &
NGROK_PID=$!

trap 'kill $NGROK_PID $APP_PID' EXIT
wait
