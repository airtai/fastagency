# update pip
pip install --upgrade pip

# install dev packages
pip install -e ".[dev-ag2]"

# install pre-commit hook if not installed already
pre-commit install
