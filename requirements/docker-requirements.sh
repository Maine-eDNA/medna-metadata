# Ubuntu 20.04
# sudo bash ubuntu-requirements.sh
apt-get update && apt-get install -y --no-install-recommends apt-utils
# POSTGRES, VIM, NETCAT
apt-get install -y netcat vim \
  libpq-dev postgresql postgresql-contrib
# GDAL, GEOS, PROJ.4, python deps
apt-get install -y \
 binutils libproj-dev gdal-bin \
 python3-dev python3-pip python3-venv python3-wheel
# PostGIS
apt-get install -y \
 postgis postgresql-12-postgis-3
# GIT
apt-get install -y \
 git
