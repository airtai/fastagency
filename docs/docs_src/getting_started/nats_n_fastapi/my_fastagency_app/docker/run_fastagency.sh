#!/bin/bash

# Accept env variable for PORT

NATS_FASTAPI_PORT=${NATS_FASTAPI_PORT:-8000}


FASTAPI_PORT=${FASTAPI_PORT:-8008}


MESOP_PORT=${MESOP_PORT:-8888}

# Default number of workers if not set
WORKERS=${WORKERS:-1}

# Run nats uvicorn server
uvicorn my_fastagency_app.deployment.main_1_nats:app --host 0.0.0.0 --port $NATS_FASTAPI_PORT > /dev/stdout 2>&1 &

# Run uvicorn server
uvicorn my_fastagency_app.deployment.main_2_fastapi:app --host 0.0.0.0 --port $FASTAPI_PORT > /dev/stdout 2>&1 &

# Run gunicorn server
gunicorn --workers=$WORKERS my_fastagency_app.deployment.main_3_mesop:app --bind 0.0.0.0:$MESOP_PORT
