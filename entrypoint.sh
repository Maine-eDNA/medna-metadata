#!/bin/bash

set -e

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

if [ "$ENTRYPOINT_DATABASE" = "postgres" ]
then
  echo "Waiting for postgres ..."
  echo "${0}: [$(date -u)] $DJANGO_DATABASE_HOST $DJANGO_DATABASE_PORT"
  while ! nc -z $DJANGO_DATABASE_HOST $DJANGO_DATABASE_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ "$ENTRYPOINT_MESSAGING" = "rabbitmq" ]
then
  echo "Waiting for rabbitmq ..."
  echo "${0}: [$(date -u)] $RABBITMQ_HOST $RABBITMQ_PORT"
  while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
    sleep 0.1
  done

  echo "RabbitMQ started"
fi

exec "$@"