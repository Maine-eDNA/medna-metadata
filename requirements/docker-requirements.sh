# Ubuntu 20.04
# sudo bash ubuntu-requirements.sh
apt-get update && apt-get install -y --no-install-recommends apt-utils
# VIM text editor
apt update && apt -y install \
 vim
# GDAL, GEOS, PROJ.4, python deps
apt-get -y install \
 binutils libproj-dev gdal-bin \
 python3-dev python3-pip python3-venv python3-wheel
# GIT
apt-get -y install \
 git