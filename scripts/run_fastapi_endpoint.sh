#!/usr/bin/env bash
set -e

HOST="0.0.0.0"
PORT="8000"
APP_MODULE="api:app"

echo "Starting FastAPI server..."
uvicorn "$APP_MODULE" \
  --host "$HOST" \
  --port "$PORT" \
  --reload
