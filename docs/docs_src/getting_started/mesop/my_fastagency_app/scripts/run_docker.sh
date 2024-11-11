#!/bin/bash

docker run -it -e OPENAI_API_KEY=$OPENAI_API_KEY   -p 8888:8888  deploy_fastagency
