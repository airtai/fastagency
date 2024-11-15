#!/bin/bash

echo -e "\033[0;32mBuilding fastagency docker image\033[0m"
docker build -t deploy_fastagency -f docker/Dockerfile --progress plain . && \
echo -e "\033[0;32mSuccessfully built fastagency docker image\033[0m"
