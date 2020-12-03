#!/usr/bin/env sh

docker run --rm --name moneytransfer-postgres \
    -e POSTGRES_PASSWORD=pass \
    -e POSTGRES_USER=interview_dbuser \
    -e POSTGRES_DB=interview \
    -p 5432:5432 \
    postgres:11.2-alpine

# docker run --rm --name moneytransfer-postgres -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=interview_dbuser -e POSTGRES_DB=interview -p 5432:5432 postgres:11.2-alpine