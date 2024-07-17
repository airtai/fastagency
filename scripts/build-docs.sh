#!/usr/bin/env bash

set -e
set -x

rm -rf docs/docs/en/api
cd docs; python docs.py build
