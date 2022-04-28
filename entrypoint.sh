#!/bin/bash

set -e

# set variables
APP_HOME=/home/django/medna-metadata
FIXTURES_DIR=${APP_HOME}/fixtures/prod

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

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
  # Run and apply database migrations
  echo "${0}: [$(date -u)] ***Applying database migrations***"
  echo "${0}: [$(date -u)] ${APP_HOME}"
  python ${APP_HOME}/manage.py migrate users
  python ${APP_HOME}/manage.py migrate utility
  python ${APP_HOME}/manage.py migrate field_site
  python ${APP_HOME}/manage.py migrate sample_label
  python ${APP_HOME}/manage.py migrate field_survey
  python ${APP_HOME}/manage.py migrate wet_lab
  python ${APP_HOME}/manage.py migrate freezer_inventory
  python ${APP_HOME}/manage.py migrate bioinfo
  python ${APP_HOME}/manage.py migrate
fi

if [ "x$DJANGO_SUPERUSER_CREATE" = 'xon' ]; then
	# PW and USERNAME supplied in medna.env
  # DJANGO_SUPERUSER_PASSWORD, DJANGO_SUPERUSER_EMAIL
	echo "${0}: [$(date -u)] ***Creating superuser"
	python ${APP_HOME}/manage.py createsuperuser --no-input
fi

if [ "x$DJANGO_DEFAULT_GROUPS_CREATE" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Creating permissions groups"
 	python ${APP_HOME}/manage.py create_default_groups
fi

if [ "x$DJANGO_DEFAULT_USERS_CREATE" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Creating default user"
 	python ${APP_HOME}/manage.py create_default_user
fi

if [ "x$DJANGO_DATABASE_FLUSH" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Flushing database"
 	python ${APP_HOME}/manage.py flush --no-input
fi

if [ "x$DJANGO_DATABASE_LOADDATA" = 'xon' ]; then
	# Load fixtures
	echo "${0}: [$(date -u)] ***Loading fixtures"
	# utility
	echo "${0}: [$(date -u)] ***Loading utility_defaultsitecss"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/utility_defaultsitecss.json
  # field_site
  echo "${0}: [$(date -u)] ***Loading field_site_system"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_system.json
  echo "${0}: [$(date -u)] ***Loading field_site_watershed"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_watershed.json
  # sample_label
  echo "${0}: [$(date -u)] ***Loading sample_label_sampletype"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/sample_label_sampletype.json
  echo "${0}: [$(date -u)] ***Loading sample_label_samplematerial"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/sample_label_samplematerial.json
  # field_survey
  echo "${0}: [$(date -u)] ***Loading field_survey_envmeasuretype"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_envmeasuretype.json
  # freezer_inventory
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_returnaction"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_returnaction.json

fi

if [ "x$DJANGO_COLLECT_STATIC" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Collecting staticfiles"
 	python ${APP_HOME}/manage.py collectstatic --noinput --clear
fi

# Start server
echo "${0}: [$(date -u)] ***Starting server"
gunicorn --bind 0.0.0.0:8000 medna_metadata.wsgi \
--workers $CELERYD_NUM_NODES --log-level=info \
--log-syslog || exit 1

exec "$@"