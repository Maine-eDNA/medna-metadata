# Ubuntu 20.04
# sudo bash ubuntu-requirements.sh
apt-get update && apt-get install -y --no-install-recommends apt-utils build-essential
# VIM, NETCAT, GIT, translations dependencies
apt-get install -y netcat vim git gettext
# python deps
apt-get install -y python3-dev python3-pip python3-venv python3-wheel
# GDAL, GEOS, PROJ.4
apt-get install -y binutils libproj-dev gdal-bin
# POSTGRES, PostGIS
apt-get install -y libpq-dev postgresql postgresql-contrib postgis postgresql-12-postgis-3
