#!/bin/bash

# Accept env variable for PORT
FASTAPI_PORT=${FASTAPI_PORT:-8008}
MESOP_PORT=${MESOP_PORT:-8888}

# Default number of workers if not set
WORKERS=${WORKERS:-1}

# Run uvicorn server
uvicorn main_1_fastapi:app --host 0.0.0.0 --port $FASTAPI_PORT > /dev/stdout 2>&1 &

# Run gunicorn server
gunicorn --workers=$WORKERS main_2_mesop:app --bind 0.0.0.0:$MESOP_PORT
