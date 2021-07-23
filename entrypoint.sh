#!/bin/bash

set -e

if [ "$ENTRYPOINT_DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DJANGO_DATABASE_HOST $DJANGO_DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
exec "$@"