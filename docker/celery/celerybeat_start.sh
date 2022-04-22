#!/bin/bash

set -o errexit
set -o nounset

celery -A medna_metadata.celery.app beat -l INFO