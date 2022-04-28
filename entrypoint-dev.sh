#!/bin/bash

set -e

# set variables
# set variables
APP_HOME=/home/django/medna-metadata
FIXTURES_DIR=${APP_HOME}/fixtures/demo

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
	echo "${0}: [$(date -u)] ***Loading utility_grant"
	python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/utility_grant.json
	echo "${0}: [$(date -u)] ***Loading utility_project"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/utility_project.json
  echo "${0}: [$(date -u)] ***Loading utility_publication"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/utility_publication.json
  echo "${0}: [$(date -u)] ***Loading utility_processlocation"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/utility_processlocation.json
  echo "${0}: [$(date -u)] ***Loading utility_standardoperatingprocedure"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/utility_standardoperatingprocedure.json
  echo "${0}: [$(date -u)] ***Loading utility_defaultsitecss"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/utility_defaultsitecss.json
  # field_site
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomefirst"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomefirst.json
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomesecond"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomesecond.json
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomethird"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomethird.json
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomefourth"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomefourth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomefifth"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomefifth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturefirst"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturefirst.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturesecond"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturesecond.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturethird"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturethird.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturefourth"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturefourth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturefifth"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturefifth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturesixth"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturesixth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeatureseventh"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_envofeatureseventh.json
  echo "${0}: [$(date -u)] ***Loading field_site_system"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_system.json
  echo "${0}: [$(date -u)] ***Loading field_site_watershed"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_watershed.json
  echo "${0}: [$(date -u)] ***Loading field_site_fieldsite"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_site_fieldsite.json
  # sample_label
  echo "${0}: [$(date -u)] ***Loading sample_label_sampletype"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/sample_label_sampletype.json
  echo "${0}: [$(date -u)] ***Loading sample_label_samplematerial"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/sample_label_samplematerial.json
  echo "${0}: [$(date -u)] ***Loading sample_label_samplelabelrequest"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/sample_label_samplelabelrequest.json
  echo "${0}: [$(date -u)] ***Loading sample_label_samplebarcode"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/sample_label_samplebarcode.json
  # field_survey
  echo "${0}: [$(date -u)] ***Loading field_survey_envmeasuretype"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_envmeasuretype.json
  echo "${0}: [$(date -u)] ***Loading field_survey_fieldsurvey"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_fieldsurvey.json
  echo "${0}: [$(date -u)] ***Loading field_survey_fieldcrew"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_fieldcrew.json
  echo "${0}: [$(date -u)] ***Loading field_survey_envmeasurement"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_envmeasurement.json
  echo "${0}: [$(date -u)] ***Loading field_survey_fieldcollection"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_fieldcollection.json
  echo "${0}: [$(date -u)] ***Loading field_survey_watercollection"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_watercollection.json
  echo "${0}: [$(date -u)] ***Loading field_survey_sedimentcollection"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_sedimentcollection.json
  echo "${0}: [$(date -u)] ***Loading field_survey_fieldsample"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_fieldsample.json
  echo "${0}: [$(date -u)] ***Loading field_survey_filtersample"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_filtersample.json
  echo "${0}: [$(date -u)] ***Loading field_survey_subcoresample"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/field_survey_subcoresample.json
  # wet_lab
  echo "${0}: [$(date -u)] ***Loading wet_lab_primerpair"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_primerpair.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_indexpair"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_indexpair.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_indexremovalmethod"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_indexremovalmethod.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_sizeselectionmethod"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_sizeselectionmethod.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_quantificationmethod"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_quantificationmethod.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_amplificationmethod"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_amplificationmethod
  echo "${0}: [$(date -u)] ***Loading wet_lab_extractionmethod"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_extractionmethod.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_extraction"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_extraction.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_pcrreplicates"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_pcrreplicates.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_pcr"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_pcr.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_libraryprep"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_libraryprep.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_pooledlibrary"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_pooledlibrary.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_runprep"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_runprep.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_runresult"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_runresult.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_fastqfile"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/wet_lab_fastqfile.json
  # freezer_inventory
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_returnaction"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_returnaction.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezer"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezer.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerrack"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerrack.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerbox"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerbox.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerinventory"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerinventory.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerinventorylog"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerinventorylog.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerinventoryreturn"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerinventoryreturn.json
  # bioinfo
  echo "${0}: [$(date -u)] ***Loading bioinfo_qualitymetadata"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_qualitymetadata.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_denoiseclustermethod"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_denoiseclustermethod.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_denoiseclustermetadata"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_denoiseclustermetadata.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_featureoutput"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_featureoutput.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_featureread"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_featureread.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxondomain"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxondomain.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonkingdom"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonkingdom.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonsupergroup"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonsupergroup.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonphylumdivision"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonphylumdivision.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonclass"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonclass.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonorder"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonorder.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonfamily"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonfamily.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxongenus"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxongenus.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonspecies"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonspecies.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_annotationmethod"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_annotationmethod.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_referencedatabase"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_referencedatabase.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_annotationmetadata"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_annotationmetadata.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonomicannotation"
  python ${APP_HOME}/manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonomicannotation.json
fi

# Start server
echo "${0}: [$(date -u)] ***Starting server"
gunicorn --bind 0.0.0.0:8000 medna_metadata.wsgi \
--workers $CELERYD_NUM_NODES --log-level=info \
--log-syslog || exit 1

exec "$@"