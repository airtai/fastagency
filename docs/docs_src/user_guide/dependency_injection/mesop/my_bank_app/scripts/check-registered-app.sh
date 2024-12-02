#!/bin/bash

# Check file registered_app_domain.txt exists. If it does not exists, echo and exit.
if [ ! -f registered_app_domain.txt ]; then
  echo -e "\033[0;33mWarning: App name is not registered.\033[0m"
  echo -e "\033[0;33mGithub Actions may fail if you push without registering.\033[0m"
  echo -e "\033[0;33mRegister your app name by running the script 'scripts/register_to_fly_io.sh'.\033[0m"
fi
