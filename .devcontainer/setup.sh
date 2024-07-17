# update pip
pip install --upgrade pip

# install dev packages
pip install -e ".[dev]"

# install pre-commit hook if not installed already
pre-commit install

# create .mypy_cache directory (see https://github.com/python/mypy/issues/10768#issuecomment-2178450153)
mkdir .mypy_cache

# install wasp
curl -sSL https://get.wasp-lang.dev/installer.sh | sh

cd app && wasp db migrate-dev && cd ..

prisma migrate deploy
prisma generate --schema=schema.prisma --generator=pyclient

# Install packages for auth callout
cd auth_callout && pnpm install && cd ..
cd auth_callout && pnpx prisma generate --schema=packages/auth-service/schema.prisma && cd ..
