# update pip
pip install --upgrade pip

# install dev packages
pip install -e ".[dev]"

# install pre-commit hook if not installed already
pre-commit install

# install wasp
curl -sSL https://get.wasp-lang.dev/installer.sh | sh -s -- -v 0.14.0

cd app && wasp db migrate-dev && cd ..

prisma migrate deploy --schema=schema.prisma
prisma generate --schema=schema.prisma --generator=pyclient

# Install packages for auth callout
cd auth_callout && pnpm install && cd ..
cd auth_callout && pnpx prisma generate --schema=packages/auth-service/schema.prisma && cd ..
