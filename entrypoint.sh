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
	# Apply createsuperuser
	echo "${0}: [$(date -u)] ***Creating superuser"
	python manage.py createsuperuser --no-input
fi

if [ "x$DJANGO_DEFAULT_GROUPS_CREATE" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Creating permissions groups"
 	python manage.py create_default_groups
fi

if [ "x$DJANGO_DEFAULT_USERS_CREATE" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Creating default users"
 	python manage.py loaddata fixtures/prod/medna_metadata_default_usernames.json
fi

if [ "x$DJANGO_DATABASE_FLUSH" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Flushing database"
 	python manage.py flush --no-input
fi

if [ "x$DJANGO_DATABASE_LOADDATA" = 'xon' ]; then
	# Load fixtures
	echo "${0}: [$(date -u)] ***Loading fixtures"
	# utility
	python manage.py loaddata fixtures/prod/utility_grant.json
  python manage.py loaddata fixtures/prod/utility_project.json
  python manage.py loaddata fixtures/prod/utility_processlocation.json
  # field_site
  python manage.py loaddata fixtures/prod/field_site_envobiomefirst.json
  python manage.py loaddata fixtures/prod/field_site_envobiomesecond.json
  python manage.py loaddata fixtures/prod/field_site_envobiomethird.json
  python manage.py loaddata fixtures/prod/field_site_envobiomefourth.json
  python manage.py loaddata fixtures/prod/field_site_envobiomefifth.json
  python manage.py loaddata fixtures/prod/field_site_envofeaturefirst.json
  python manage.py loaddata fixtures/prod/field_site_envofeaturesecond.json
  python manage.py loaddata fixtures/prod/field_site_envofeaturethird.json
  python manage.py loaddata fixtures/prod/field_site_envofeaturefourth.json
  python manage.py loaddata fixtures/prod/field_site_envofeaturefifth.json
  python manage.py loaddata fixtures/prod/field_site_envofeaturesixth.json
  python manage.py loaddata fixtures/prod/field_site_envofeatureseventh.json
  python manage.py loaddata fixtures/prod/field_site_system.json
  python manage.py loaddata fixtures/prod/field_site_watershed.json
  python manage.py loaddata fixtures/prod/field_site_fieldsite.json
  # sample_label
  python manage.py loaddata fixtures/prod/sample_label_sampletype.json
  python manage.py loaddata fixtures/prod/sample_label_samplematerial.json
  python manage.py loaddata fixtures/prod/sample_label_samplelabelrequest.json
  python manage.py loaddata fixtures/prod/sample_label_samplebarcode.json
  # field_survey_etl
  python manage.py loaddata fixtures/prod/field_survey_fieldsurveyetl.json
  python manage.py loaddata fixtures/prod/field_survey_fieldcrewetl.json
  python manage.py loaddata fixtures/prod/field_survey_envmeasurementetl.json
  python manage.py loaddata fixtures/prod/field_survey_fieldcollectionetl.json
  python manage.py loaddata fixtures/prod/field_survey_samplefilteretl.json
  # field_survey
  python manage.py loaddata fixtures/prod/field_survey_fieldsurvey.json
  python manage.py loaddata fixtures/prod/field_survey_fieldcrew.json
  python manage.py loaddata fixtures/prod/field_survey_envmeasurement.json
  python manage.py loaddata fixtures/prod/field_survey_fieldcollection.json
  python manage.py loaddata fixtures/prod/field_survey_watercollection.json
  python manage.py loaddata fixtures/prod/field_survey_sedimentcollection.json
  python manage.py loaddata fixtures/prod/field_survey_fieldsample.json
  python manage.py loaddata fixtures/prod/field_survey_filtersample.json
  python manage.py loaddata fixtures/prod/field_survey_subcoresample.json
  # wet_lab
  python manage.py loaddata fixtures/prod/wet_lab_primerpair.json
  python manage.py loaddata fixtures/prod/wet_lab_indexremovalmethod.json
  python manage.py loaddata fixtures/prod/wet_lab_sizeselectionmethod.json
  python manage.py loaddata fixtures/prod/wet_lab_quantificationmethod.json
  python manage.py loaddata fixtures/prod/wet_lab_extractionmethod.json
  python manage.py loaddata fixtures/prod/wet_lab_indexpair.json
  python manage.py loaddata fixtures/prod/wet_lab_extraction.json
  python manage.py loaddata fixtures/prod/wet_lab_libraryprep.json
  python manage.py loaddata fixtures/prod/wet_lab_pooledlibrary.json
  python manage.py loaddata fixtures/prod/wet_lab_runprep.json
  python manage.py loaddata fixtures/prod/wet_lab_runresult.json
  # freezer_inventory
  python manage.py loaddata fixtures/prod/freezer_inventory_freezer.json
  python manage.py loaddata fixtures/prod/freezer_inventory_freezerrack.json
  python manage.py loaddata fixtures/prod/freezer_inventory_freezerbox.json
  python manage.py loaddata fixtures/prod/freezer_inventory_freezerinventory.json
  python manage.py loaddata fixtures/prod/freezer_inventory_freezerinventorylog.json
  python manage.py loaddata fixtures/prod/freezer_inventory_freezerinventoryreturn.json
  # bioinfo
  python manage.py loaddata fixtures/prod/bioinfo_denoiseclustermethod.json
  python manage.py loaddata fixtures/prod/bioinfo_denoiseclustermetadata.json
  python manage.py loaddata fixtures/prod/bioinfo_featureoutput.json
  python manage.py loaddata fixtures/prod/bioinfo_featureread.json
  python manage.py loaddata fixtures/prod/bioinfo_referencedatabase.json
  python manage.py loaddata fixtures/prod/bioinfo_taxondomain.json
  python manage.py loaddata fixtures/prod/bioinfo_taxonkingdom.json
  python manage.py loaddata fixtures/prod/bioinfo_taxonphylumdivision.json
  python manage.py loaddata fixtures/prod/bioinfo_taxonclass.json
  python manage.py loaddata fixtures/prod/bioinfo_taxonorder.json
  python manage.py loaddata fixtures/prod/bioinfo_taxonfamily.json
  python manage.py loaddata fixtures/prod/bioinfo_taxongenus.json
  python manage.py loaddata fixtures/prod/bioinfo_taxonspecies.json
  python manage.py loaddata fixtures/prod/bioinfo_annotationmethod.json
  python manage.py loaddata fixtures/prod/bioinfo_annotationmetadata.json
  python manage.py loaddata fixtures/prod/bioinfo_taxonomicannotation.json
fi

# Start server
echo "${0}: [$(date -u)] ***Starting server"
gunicorn --bind 0.0.0.0:8000 medna_metadata.wsgi \
--workers 3 --log-level=info \
--log-syslog || exit 1

exec "$@"