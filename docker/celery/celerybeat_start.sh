#!/bin/bash

set -o errexit
set -o nounset

celery -A medna_metadata beat -l INFO