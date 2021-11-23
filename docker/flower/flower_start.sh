#!/bin/bash

set -o errexit
set -o nounset

worker_ready() {
    celery -A medna_metadata inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers is available'

celery -A medna_metadata  \
    --broker="${CELERY_BROKER_URL}" \
    flower