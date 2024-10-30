#!/bin/sh

black .

alembic upgrade head

exec "$@"