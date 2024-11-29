#!/bin/bash


# Check file registered_app_domain.txt exists. If it does, echo and exit.
if [ -f registered_app_domain.txt ]; then
    echo -e "\033[1;33mWarning: App name is already registered.\033[0m"
    echo -e "\033[0;32mRegistered app name is:\033[0m"
    cat registered_app_domain.txt
    exit 1
fi

echo -e "\033[0;32mChecking if already logged into fly.io\033[0m"
if ! flyctl auth whoami > /dev/null 2>&1; then
    echo -e "\033[0;32mLogging into fly.io\033[0m"
    flyctl auth login
else
    echo -e "\033[0;32mAlready logged into fly.io\033[0m"
fi

export FLY_APP_NAME=$(grep "^app = " fly.toml | awk -F"'" '{print $2}')

echo -e "\033[0;32mRegistering app name in fly.io\033[0m"
if flyctl apps create $FLY_APP_NAME; then
    echo "$FLY_APP_NAME.fly.dev" > registered_app_domain.txt
    echo -e "\033[0;32mApp name registered successfully\033[0m"
    echo -e "\033[0;32mRegistered app name is:\033[0m"
    cat registered_app_domain.txt
else
    echo -e "\033[1;31mError: App name is not available.\033[0m"
    echo -e "\033[1;31mPlease change the app name in fly.toml and run this script again.\033[0m"
    exit 1
fi
