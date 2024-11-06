#!/bin/bash

docker build -t deploy_fastagency -f docker/Dockerfile --progress plain .
