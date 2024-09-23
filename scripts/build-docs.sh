#!/usr/bin/env bash

export TERMINAL_WIDTH=80

set -e
set -x

cd docs; python docs.py build
