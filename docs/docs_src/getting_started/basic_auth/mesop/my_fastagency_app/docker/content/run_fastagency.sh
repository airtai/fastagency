#!/bin/bash

# Accept env variable for PORT



export MESOP_PORT=${MESOP_PORT:-8888}
export SERVICE_PORT=$MESOP_PORT

# Default number of workers if not set
WORKERS=${WORKERS:-1}
echo "Number of workers: $WORKERS"

# Check FLY_MACHINE_ID is set, if not set, set it to dummy value
export FLY_MACHINE_ID=${FLY_MACHINE_ID:-dummy_fly_machine_id_value}
echo "Fly machine ID: $FLY_MACHINE_ID"

# Generate nginx config
for ((i=1; i<$WORKERS+1; i++))
do
	PORT=$((SERVICE_PORT + i))
    sed -i "5i\    server 127.0.0.1:$PORT;" nginx.conf.template
done
envsubst '${SERVICE_PORT},${FLY_MACHINE_ID}' < nginx.conf.template >/etc/nginx/conf.d/default.conf
echo "Nginx config:"
cat /etc/nginx/conf.d/default.conf

# Start nginx
nginx -g "daemon off;" &


# Run uvicorn server
uvicorn my_fastagency_app.deployment.main_:app --host 0.0.0.0 --port $FASTAPI_PORT > /dev/stdout 2>&1 &


# Run gunicorn server
# Start multiple single-worker gunicorn instances on consecutive ports
for ((i=1; i<$WORKERS+1; i++))
do
	PORT=$((SERVICE_PORT + i))
    echo "Starting gunicorn on port $PORT"
    gunicorn --workers=1 my_fastagency_app.deployment.main:app --bind 0.0.0.0:$PORT > /dev/stdout 2>&1 &
done

# Wait for all background processes
wait
