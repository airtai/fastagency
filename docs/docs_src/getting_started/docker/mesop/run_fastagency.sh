#!/bin/bash

# Accept env variable for PORT, set 8000 as default port
MESOP_PORT=${MESOP_PORT:-8000}

# Default number of workers if not set
WORKERS=${WORKERS:-1}

# Run gunicorn server
gunicorn --workers=$WORKERS main_mesop:app --bind 0.0.0.0:$MESOP_PORT
