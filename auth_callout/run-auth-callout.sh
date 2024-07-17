#!/bin/sh

pnpx prisma generate --schema=packages/auth-service/schema.prisma

pnpm serve
