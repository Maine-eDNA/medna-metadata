#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A medna_metadata.celery.app beat -l INFO