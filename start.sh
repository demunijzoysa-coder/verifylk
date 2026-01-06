#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"
VENV="$BACKEND/.venv"

if [ ! -d "$VENV" ]; then
  echo "Creating backend virtualenv..."
  python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"

if [ "$1" != "--skip-install" ]; then
  echo "Installing backend requirements..."
  pip install -r "$BACKEND/requirements.txt"
  echo "Installing frontend dependencies..."
  (cd "$FRONTEND" && npm install)
fi

echo "Launching backend..."
(cd "$BACKEND" && "$VENV/bin/python" -m uvicorn app.main:app --reload) &
BACK_PID=$!

echo "Launching frontend..."
(cd "$FRONTEND" && npm run dev) &
FRONT_PID=$!

trap "kill $BACK_PID $FRONT_PID" EXIT
echo "Backend: http://127.0.0.1:8000  |  Frontend: http://127.0.0.1:5173"
wait
