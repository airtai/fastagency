#!/bin/bash

echo -e "\033[0;32mLogging into fly.io\033[0m"
fly auth login

echo -e "\033[0;32mDeploying to fly.io\033[0m"
fly launch --config fly.toml --copy-config --yes

echo -e "\033[0;32mSetting secrets\033[0m"
fly secrets set OPENAI_API_KEY=$OPENAI_API_KEY
