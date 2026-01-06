#!/usr/bin/env bash
set +e
echo "Stopping VerifyLK services..."
for port in 8000 5173; do
  pid=$(lsof -t -i:$port)
  if [ -n "$pid" ]; then
    echo "Killing process on port $port (PID $pid)"
    kill "$pid"
  fi
done
echo "Done. Close any dev terminals if still running."
