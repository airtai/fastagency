#!/bin/bash

docker run -d --name deploy_fastagency -e OPENAI_API_KEY=$OPENAI_API_KEY  -p 8888:8888  deploy_fastagency
