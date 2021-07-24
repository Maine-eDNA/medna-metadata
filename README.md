# medna-metadata
Maine-eDNA metadata - a data management system for tracking environmental DNA samples

The `/docker` directory has `medna.env.db.txt`, `medna.env.txt`, and `nginx.proxycompanion.env.txt` which contain 
all environmental variables for docker deployment. Make a copy of these files with the `.txt` extension removed 
(e.g., `medna.env.db`, `medna.env`, `nginx.proxycompanion.env`) and variables updated with desired settings. 
These files are necessary for docker. Other files that affect docker are:
* `entrypoint.sh`
* `.dockerignore`
* contents of `/docker` directory
* settings in `medna_metadata/settings.py`


Once settings are verified, run `sudo docker-comopse up -d` to build and deploy medna-metadata, PostgreSQL with PostGIS, 
and NGINX with LetsEncrypt.