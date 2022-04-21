#!/bin/bash

set -e

# set variables
FIXTURES_DIR=fixtures/demo

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
 	python manage.py loaddata ${FIXTURES_DIR}/medna_metadata_demo_usernames.json
fi

if [ "x$DJANGO_DATABASE_FLUSH" = 'xon' ]; then
 	echo "${0}: [$(date -u)] ***Flushing database"
 	python manage.py flush --no-input
fi

if [ "x$DJANGO_DATABASE_LOADDATA" = 'xon' ]; then
	# Load fixtures
	echo "${0}: [$(date -u)] ***Loading fixtures"
	# utility
	echo "${0}: [$(date -u)] ***Loading utility_grant"
	python manage.py loaddata ${FIXTURES_DIR}/utility_grant.json
	echo "${0}: [$(date -u)] ***Loading utility_project"
  python manage.py loaddata ${FIXTURES_DIR}/utility_project.json
  echo "${0}: [$(date -u)] ***Loading utility_publication"
  python manage.py loaddata ${FIXTURES_DIR}/utility_publication.json
  echo "${0}: [$(date -u)] ***Loading utility_processlocation"
  python manage.py loaddata ${FIXTURES_DIR}/utility_processlocation.json
  echo "${0}: [$(date -u)] ***Loading utility_standardoperatingprocedure"
  python manage.py loaddata ${FIXTURES_DIR}/utility_standardoperatingprocedure.json
  echo "${0}: [$(date -u)] ***Loading utility_defaultsitecss"
  python manage.py loaddata ${FIXTURES_DIR}/utility_defaultsitecss.json
  # field_site
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomefirst"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomefirst.json
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomesecond"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomesecond.json
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomethird"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomethird.json
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomefourth"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomefourth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envobiomefifth"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envobiomefifth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturefirst"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturefirst.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturesecond"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturesecond.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturethird"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturethird.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturefourth"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturefourth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturefifth"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturefifth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeaturesixth"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envofeaturesixth.json
  echo "${0}: [$(date -u)] ***Loading field_site_envofeatureseventh"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_envofeatureseventh.json
  echo "${0}: [$(date -u)] ***Loading field_site_system"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_system.json
  echo "${0}: [$(date -u)] ***Loading field_site_watershed"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_watershed.json
  echo "${0}: [$(date -u)] ***Loading field_site_fieldsite"
  python manage.py loaddata ${FIXTURES_DIR}/field_site_fieldsite.json
  # sample_label
  echo "${0}: [$(date -u)] ***Loading sample_label_sampletype"
  python manage.py loaddata ${FIXTURES_DIR}/sample_label_sampletype.json
  echo "${0}: [$(date -u)] ***Loading sample_label_samplematerial"
  python manage.py loaddata ${FIXTURES_DIR}/sample_label_samplematerial.json
  echo "${0}: [$(date -u)] ***Loading sample_label_samplelabelrequest"
  python manage.py loaddata ${FIXTURES_DIR}/sample_label_samplelabelrequest.json
  echo "${0}: [$(date -u)] ***Loading sample_label_samplebarcode"
  python manage.py loaddata ${FIXTURES_DIR}/sample_label_samplebarcode.json
  # field_survey
  echo "${0}: [$(date -u)] ***Loading field_survey_envmeasuretype"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_envmeasuretype.json
  echo "${0}: [$(date -u)] ***Loading field_survey_fieldsurvey"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_fieldsurvey.json
  echo "${0}: [$(date -u)] ***Loading field_survey_fieldcrew"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_fieldcrew.json
  echo "${0}: [$(date -u)] ***Loading field_survey_envmeasurement"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_envmeasurement.json
  echo "${0}: [$(date -u)] ***Loading field_survey_fieldcollection"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_fieldcollection.json
  echo "${0}: [$(date -u)] ***Loading field_survey_watercollection"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_watercollection.json
  echo "${0}: [$(date -u)] ***Loading field_survey_sedimentcollection"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_sedimentcollection.json
  echo "${0}: [$(date -u)] ***Loading field_survey_fieldsample"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_fieldsample.json
  echo "${0}: [$(date -u)] ***Loading field_survey_filtersample"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_filtersample.json
  echo "${0}: [$(date -u)] ***Loading field_survey_subcoresample"
  python manage.py loaddata ${FIXTURES_DIR}/field_survey_subcoresample.json
  # wet_lab
  echo "${0}: [$(date -u)] ***Loading wet_lab_primerpair"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_primerpair.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_indexpair"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_indexpair.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_indexremovalmethod"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_indexremovalmethod.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_sizeselectionmethod"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_sizeselectionmethod.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_quantificationmethod"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_quantificationmethod.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_amplificationmethod"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_amplificationmethod
  echo "${0}: [$(date -u)] ***Loading wet_lab_extractionmethod"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_extractionmethod.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_extraction"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_extraction.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_pcrreplicates"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_pcrreplicates.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_pcr"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_pcr.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_libraryprep"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_libraryprep.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_pooledlibrary"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_pooledlibrary.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_runprep"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_runprep.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_runresult"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_runresult.json
  echo "${0}: [$(date -u)] ***Loading wet_lab_fastqfile"
  python manage.py loaddata ${FIXTURES_DIR}/wet_lab_fastqfile.json
  # freezer_inventory
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_returnaction"
  python manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_returnaction.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezer"
  python manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezer.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerrack"
  python manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerrack.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerbox"
  python manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerbox.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerinventory"
  python manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerinventory.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerinventorylog"
  python manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerinventorylog.json
  echo "${0}: [$(date -u)] ***Loading freezer_inventory_freezerinventoryreturn"
  python manage.py loaddata ${FIXTURES_DIR}/freezer_inventory_freezerinventoryreturn.json
  # bioinfo
  echo "${0}: [$(date -u)] ***Loading bioinfo_qualitymetadata"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_qualitymetadata.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_denoiseclustermethod"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_denoiseclustermethod.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_denoiseclustermetadata"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_denoiseclustermetadata.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_featureoutput"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_featureoutput.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_featureread"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_featureread.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxondomain"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxondomain.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonkingdom"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonkingdom.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonsupergroup"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonsupergroup.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonphylumdivision"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonphylumdivision.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonclass"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonclass.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonorder"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonorder.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonfamily"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonfamily.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxongenus"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxongenus.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonspecies"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonspecies.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_annotationmethod"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_annotationmethod.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_referencedatabase"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_referencedatabase.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_annotationmetadata"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_annotationmetadata.json
  echo "${0}: [$(date -u)] ***Loading bioinfo_taxonomicannotation"
  python manage.py loaddata ${FIXTURES_DIR}/bioinfo_taxonomicannotation.json
fi

# Start server
echo "${0}: [$(date -u)] ***Starting server"
gunicorn --bind 0.0.0.0:8000 medna_metadata.wsgi \
--workers $CELERYD_NUM_NODES --log-level=info \
--log-syslog || exit 1

exec "$@"