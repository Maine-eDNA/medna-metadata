# medna-metadata
Maine-eDNA metadata - a data management system for tracking environmental DNA samples

The `/docker` directory contains `medna.env.db.txt`, `medna.env.txt`, and `nginx.proxycompanion.env.txt` which contain 
all environmental variables for deployment. Make a copy of these files with the `.txt` extension removed 
(e.g., `medna.env.db`, `medna.env`, `nginx.proxycompanion.env`) and variables updated with desired settings. 
These files are necessary for docker. Other files necessary for docker are:
* `entrypoint.sh`
* `.dockerignore`
* contents of `/docker` directory