#!/bin/bash
set -e
export REDIS_URL=${REDIS_URL:-redis://localhost:6379/0}
export STORAGE_DIR=${STORAGE_DIR:-/tmp/flashai_storage}
mkdir -p "$STORAGE_DIR"
echo "Start uvicorn..."
python3 -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 &
sleep 2
echo "Start rq worker..."
rq worker &
wait
