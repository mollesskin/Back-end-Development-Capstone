#!/bin/sh
set -eu
python manage.py migrate --noinput
# Create an administrator explicitly; never ship default credentials.
exec "$@"
