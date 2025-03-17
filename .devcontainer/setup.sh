# update pip
pip install --upgrade pip uv

# install dev packages
pip install -e ".[dev]"

# install pre-commit hook if not installed already
pre-commit install
