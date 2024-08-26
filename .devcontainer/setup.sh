# update pip
pip install --upgrade pip

# install dev packages
pip install -e ".[dev]"

# install pre-commit hook if not installed already
pre-commit install

# run wasp prisma commands
prima migrate deploy --schema=wasp_schema.prisma
prisma generate --schema=wasp_schema.prisma --generator=client

# run python prisma commands
prisma migrate deploy --schema=schema.prisma
prisma generate --schema=schema.prisma --generator=pyclient
