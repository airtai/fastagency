#!/bin/bash

docker run -d --name deploy_fastagency -e OPENAI_API_KEY=$OPENAI_API_KEY -e NATS_URL=$NATS_URL -e FASTAGENCY_NATS_PASSWORD=$FASTAGENCY_NATS_PASSWORD -p 8000:8000 -p 8008:8008 -p 8888:8888 --network=host deploy_fastagency
