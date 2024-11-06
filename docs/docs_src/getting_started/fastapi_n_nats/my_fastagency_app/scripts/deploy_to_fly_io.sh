#!/bin/bash

fly auth login

fly launch --config fly.toml --copy-config --yes

fly secrets set OPENAI_API_KEY=$OPENAI_API_KEY
