#!/bin/bash

# Accept env variable for PORT
export NATS_FASTAPI_PORT=${NATS_FASTAPI_PORT:-8000}
export FASTAPI_PORT=${FASTAPI_PORT:-8008}
export MESOP_PORT=${MESOP_PORT:-8888}

# Default number of workers if not set
WORKERS=${WORKERS:-1}
echo "Number of workers: $WORKERS"

# Check FLY_MACHINE_ID is set, if not set, set it to dummy value
export FLY_MACHINE_ID=${FLY_MACHINE_ID:-dummy_fly_machine_id_value}
echo "Fly machine ID: $FLY_MACHINE_ID"

# Generate nginx config
for ((i=1; i<$WORKERS+1; i++))
do
	PORT=$((MESOP_PORT + i))
    sed -i "19i\    server 127.0.0.1:$PORT;" nginx.conf.template
done

for ((i=1; i<$WORKERS+1; i++))
do
	PORT=$((FASTAPI_PORT + i))
    sed -i "12i\    server 127.0.0.1:$PORT;" nginx.conf.template
done

for ((i=1; i<$WORKERS+1; i++))
do
	PORT=$((NATS_FASTAPI_PORT + i))
    sed -i "5i\    server 127.0.0.1:$PORT;" nginx.conf.template
done

envsubst '${NATS_FASTAPI_PORT},${FASTAPI_PORT},${MESOP_PORT},${FLY_MACHINE_ID}' < nginx.conf.template >/etc/nginx/conf.d/default.conf
echo "Nginx config:"
cat /etc/nginx/conf.d/default.conf

# Start nginx
nginx -g "daemon off;" &



# Run gunicorn server
# Start multiple single-worker gunicorn instances on consecutive ports
for ((i=1; i<$WORKERS+1; i++))
do
	PORT=$((MESOP_PORT + i))
    echo "Starting gunicorn on port $PORT"
    gunicorn --workers=1 my_bank_app.deployment.main:app --bind 0.0.0.0:$PORT > /dev/stdout 2>&1 &
done

# Wait for all background processes
wait
