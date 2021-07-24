# Ubuntu 20.04
# sudo bash ubuntu-requirements.sh
apt-get update && apt-get install -y --no-install-recommends apt-utils
# Django with Postgres, Nginx, and Gunicorn on Ubuntu 20.04
apt update && apt -y install \
 libpq-dev postgresql postgresql-contrib nginx curl vim netcat
# GDAL, GEOS, PROJ.4, python deps
apt-get -y install \
 binutils libproj-dev gdal-bin \
 python3-dev python3-pip python3-venv python3-wheel
# PostGIS
apt -y install \
 postgis postgresql-12-postgis-3
# Certbot and Nginx plugin
apt -y install \
 certbot python3-certbot-nginx