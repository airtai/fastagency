# update pip
pip install --upgrade pip

# install dev packages
pip install -e ".[dev]"

# install pre-commit hooks
pre-commit install

# install fly.io CLI and set fly.io CLI PATH in bashrc and zshrc
curl -L https://fly.io/install.sh | sh
echo 'export FLYCTL_INSTALL="/home/vscode/.fly"' | tee -a ~/.bashrc ~/.zshrc
echo 'export PATH="$FLYCTL_INSTALL/bin:$PATH"' | tee -a ~/.bashrc ~/.zshrc

# check OPENAI_API_KEY environment variable is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo
    echo -e "\033[33mWarning: OPENAI_API_KEY environment variable is not set.\033[0m"
    echo
fi
