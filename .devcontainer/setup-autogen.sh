# update pip
pip install --upgrade pip

# install dev packages
pip install -e ".[dev-autogen]"

# install pre-commit hook if not installed already
pre-commit install
