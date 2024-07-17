#!/usr/bin/env bash

# Check the value of the DOMAIN environment variable
if [[ -z "$DOMAIN" || "$DOMAIN" == *"staging"* || "$DOMAIN" == *"localhost"* ]]; then
  workers=2
else
  workers=4
fi

prisma migrate deploy
prisma generate --schema=schema.prisma --generator=pyclient

faststream run fastagency.io.ionats:app --workers $workers > faststream.log 2>&1 &

uvicorn fastagency.app:app --workers $workers --host 0.0.0.0 --proxy-headers
