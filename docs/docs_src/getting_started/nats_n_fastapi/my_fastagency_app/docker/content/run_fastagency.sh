#!/bin/bash

# Accept env variable for PORT

NATS_FASTAPI_PORT=${NATS_FASTAPI_PORT:-8000}


FASTAPI_PORT=${FASTAPI_PORT:-8008}

export MESOP_PORT=${MESOP_PORT:-8888}

# Default number of workers if not set
WORKERS=${WORKERS:-1}
echo "Number of workers: $WORKERS"

# Generate nginx config
for ((i=1; i<$WORKERS+1; i++))
do
	PORT=$((MESOP_PORT + i))
    sed -i "5i\    server 127.0.0.1:$PORT;" nginx.conf.template
done
envsubst '${MESOP_PORT}' < nginx.conf.template >/etc/nginx/conf.d/default.conf
echo "Nginx config:"
cat /etc/nginx/conf.d/default.conf

# Start nginx
nginx -g "daemon off;" &

# Run nats uvicorn server
uvicorn my_fastagency_app.deployment.main_1_nats:app --host 0.0.0.0 --port $NATS_FASTAPI_PORT > /dev/stdout 2>&1 &

# Run uvicorn server
uvicorn my_fastagency_app.deployment.main_2_fastapi:app --host 0.0.0.0 --port $FASTAPI_PORT > /dev/stdout 2>&1 &

# Run gunicorn server
# Start multiple single-worker gunicorn instances on consecutive ports
for ((i=1; i<$WORKERS+1; i++))
do
	PORT=$((MESOP_PORT + i))
    echo "Starting gunicorn on port $PORT"
    gunicorn --workers=1 my_fastagency_app.deployment.main_3_mesop:app --bind 0.0.0.0:$PORT > /dev/stdout 2>&1 &
done

# Wait for all background processes
wait
