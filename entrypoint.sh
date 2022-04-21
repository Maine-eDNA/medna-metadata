#!/bin/bash

set -e

# set variables
FIXTURES_DIR=fixtures/prod

if [ "$ENTRYPOINT_DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DJANGO_DATABASE_HOST $DJANGO_DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
	# Run and apply database migrations
  echo "${0}: [$(date -u)] ***Applying database migrations***"
  python manage.py migrate users
  python manage.py migrate utility
  python manage.py migrate field_site
  python manage.py migrate sample_label
  python manage.py migrate field_survey
  python manage.py migrate wet_lab
  python manage.py migrate freezer_inventory
  python manage.py migrate bioinfo
  python manage.py migrate
fi

if [ "x$DJANGO_SUPERUSER_CREATE" = 'xon' ]; then
	# PW and USERNAME supplied in medna.env
  # DJANGO_SUPERUSER_PASSWORD, DJANGO_SUPERUSER_EMAIL
	echo "${0}: [$(date -u)] ***Creating superuser"
	python manage.py createsuperuser --no-input
fi

if [ "x$DJANGO_DEFAULT_GROUPS_CREATE" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Creating permissions groups"
 	python manage.py create_default_groups
fi

if [ "x$DJANGO_DEFAULT_USERS_CREATE" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Creating default users"
 	python manage.py loaddata ${FIXTURES_DIR}/medna_metadata_default_usernames.json
fi

if [ "x$DJANGO_DATABASE_FLUSH" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Flushing database"
 	python manage.py flush --no-input
fi

if [ "x$DJANGO_DATABASE_LOADDATA" = 'xon' ]; then
	# Load fixtures
	echo "${0}: [$(date -u)] ***Loading fixtures"
	# utility
	echo "${0}: [$(date -u)] ***Loading utility_defaultsitecss"
  python manage.py loaddata ${FIXTURES_DIR}/utility_defaultsitecss.json
  # field_site
  echo "${0}: [$(date -u)] ***Loading field_site_system"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_system.json
  echo "${0}: [$(date -u)] ***Loading field_site_watershed"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_watershed.json
  # sample_label
  echo "${0}: [$(date -u)] ***Loading sample_label_sampletype"
  python manage.py loaddata ${FIXTURES_DIR}/sample_label_sampletype.json
  echo "${0}: [$(date -u)] ***Loading sample_label_samplematerial"
  python manage.py loaddata ${FIXTURES_DIR}/sample_label_samplematerial.json
  # field_survey
  echo "${0}: [$(date -u)] ***Loading field_survey_envmeasuretype"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_envmeasuretype.json
  # freezer_inventory
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_returnaction"
  python manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_returnaction.json

fi

# Start server
echo "${0}: [$(date -u)] ***Starting server"
gunicorn --bind 0.0.0.0:8000 medna_metadata.wsgi \
--workers $CELERYD_NUM_NODES --log-level=info \
--log-syslog || exit 1

exec "$@"