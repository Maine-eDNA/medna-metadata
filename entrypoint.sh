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

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
	# Run and apply database migrations
	#echo "${0}: Creating database migrations"
	#python manage.py makemigrations users
	#python manage.py makemigrations field_sites
	#python manage.py makemigrations sample_labels
	echo "${0}: Applying database migrations"
	python manage.py migrate users
	python manage.py migrate field_sites
	python manage.py migrate sample_labels
	#python manage.py migrate field_survey
	#python manage.py migrate freezer_inventory
	#python manage.py migrate wet_lab
	python manage.py migrate
fi

if [ "x$DJANGO_SUPERUSER_CREATE" = 'xon' ]; then
	# Apply createsuperuser
	echo "${0}: Creating superuser"
	python manage.py createsuperuser --no-input
fi

if [ "x$DJANGO_DATABASE_LOADDATA" = 'xon' ]; then
	# Apply createsuperuser
	echo "${0}: Loading fixtures"
	python manage.py loaddata fixtures/field_sites_project.json
	python manage.py loaddata fixtures/field_sites_system.json
	python manage.py loaddata fixtures/field_sites_region.json
	python manage.py loaddata fixtures/field_sites_fieldsite.json
	python manage.py loaddata fixtures/sample_labels_SampleMaterial.json
	python manage.py loaddata fixtures/sample_labels_samplelabelrequest.json

fi

# Start server
echo "${0}: Starting server"
gunicorn --bind 0.0.0.0:8000 medna_metadata.wsgi \
--workers 3 --log-level=info \
--log-syslog || exit 1

exec "$@"