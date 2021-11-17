# Maine-eDNA metadata - a data management system for tracking environmental DNA samples
This repository contains the backend components of Maine-eDNA metadata (API, database) and was built with the [Django web framework](https://www.djangoproject.com/). 
The frontend components are located in the [medna-metadata-frontend repository](https://github.com/Maine-eDNA/medna-metadata-frontend), which is written with the [ReactJS library](https://reactjs.org/).
The frontend communicates with the backend through the API, built with the [Django REST Framework](https://www.django-rest-framework.org/).

*The Dockerfiles in /docker are not yet fully tested. Once they are this message will be updated and users can use the docker steps to deploy the django app.*
## How to setup on Ubuntu 20.04

If you've never set up a server before, DigitalOcean provides an extensive variety of tutorials that we highly recommend:
* https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04

The remaining steps were adapted from the following DigitalOcean tutorial:
* https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04

*Note that it might be useful to visit this tutorial and read the rational behind some of the steps below.*

### Install Ubuntu Requirements
```commandline
sudo bash /home/youruser/medna-metadata/requirementsubuntu-requirements.sh
```

### Create PostgreSQL database with PostGIS Extension
Create the database for your project:

```commandline
sudo -u postgres psql -c "CREATE DATABASE medna_metadata;"
```

Create a database user and add them to the project with a secure password:

```commandline
sudo -u postgres psql -c "CREATE USER django WITH PASSWORD 'your_db_password';"
```

Recommended settings from the Django project:

```commandline
sudo -u postgres psql -c "ALTER ROLE django SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE django SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE django SET timezone TO 'UTC';"
```

Set the Django user as the administrator for the medna_metadata database:

```commandline
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE medna_metadata TO django;"
```

Grant privledges to the Django database user to create databases for django tests:

```commandline
sudo -u postgres psql -c "ALTER USER django CREATEDB;"
```

Add PostGIS to medna_metadata:

```commandline
sudo -i -u postgres psql -d medna_metadata -c "CREATE EXTENSION postgis;"
```

### Create a virtual environment with venv
```commandline
sudo -H pip install --upgrade pip
sudo -H pip install virtualenvwrapper
sudo -H pip install virtualenv
```

Dotenv is a python library for reading in environmental variables from a file:

```commandline
pip install django-dotenv
```

Add environmental variables to the end of bashrc, which will reload the variables at restart.
The variables to copy into `~/.bashrc` are listed in `docker/bashrc.txt`:

```commandline
sudo vim ~/.bashrc
```

Load the environmental variables:

```commandline
source ~/.bashrc
```

To create and activate virtualenvwrapper:

```commandline
mkvirtualenv --python /usr/bin/python3.8 mednaenv
```

*Note that the version of python varies and you will have to check or install it.*
* https://stackoverflow.com/questions/6401951/using-different-versions-of-python-with-virtualenvwrapper
* https://unix.stackexchange.com/questions/410579/change-the-python3-default-version-in-ubuntu

```commandline
workon mednaenv
```

Install python requirements to the virtualenv:

```commandline
pip install -U -r /home/youruser/medna-metadata/requirements/prod.txt
```

### Migrate the database schema to PostgreSQL from within the same directory as `manage.py`
Within each app there is a migration directory which contains files which tell the database how to 
create the database tables. These have been pre-generated and added to this repository to simplify the 
process of deplying the Maine-eDNA Metadata application.
```commandline
python manage.py migrate users
python manage.py migrate utility
python manage.py migrate field_sites
python manage.py migrate sample_labels
python manage.py migrate field_survey
python manage.py migrate wet_lab
python manage.py migrate freezer_inventory
python manage.py migrate bioinfo_denoising
python manage.py migrate bioinfo_taxon
```

Now, if everything looked good (e.g., no error messages), makemigrations again and migrate
python manage.py makemigrations

```commandline
python manage.py makemigrations
python manage.py migrate
```

### Create a administrative user for the medna_metadata project

```commandline
python manage.py createsuperuser
```

Enter in your preferred credentials.

### Collect all static content into the directory specified in settings.py

```commandline
python manage.py collectstatic
```

### Test the deployment

Temporarily create an exception for port 8000

```commandline
sudo ufw allow 8000
```

Test the project deployment

```commandline
python manage.py runserver 0.0.0.0:8000
```

In your web browser, visit the server's IP address followed by :8000

`http://your_ip_address:8000`

Enter [CTRL-C] in to shut down the test deployment

Now test to see if the project can be deployed with Gunicorn:

```commandline
gunicorn --bind 0.0.0.0:8000 medna-metadata.wsgi
```

If you were able to visit the same page while deployed with Gunicorn, continue onward. If not, some helpful
troubleshooting steps can be found in the DigitalOcean tutorial on setting up Django with PostgreSQL, Gunicorn, and Nginx:
* https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04

### Create Gunicorn Socket and Service files

Leave the virtualenv:

```commandline
deactivate
```

Create a systemd Socket file:

```commandline
sudo vim /etc/systemd/system/gunicorn.socket
```

````buildoutcfg
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
````

Write and exit the VIM text editor:

```textmate
:wq!
```

Create a systemd service file:

```commandline
sudo vim /etc/systemd/system/gunicorn.service
```

```buildoutcfg
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=django
Group=django
WorkingDirectory=/home/youruser/medna-metadata
EnvironmentFile=/home/youruser/medna-metadata/docker/gunicorn.env
ExecStart=/home/youruser/.virtualenvs/mednaenv/bin/gunicorn \
          --access-logfile - --workers 3 \
          --bind unix:/run/gunicorn.sock \
          medna_metadata.wsgi:application

[Install]
WantedBy=multi-user.target
```
*Please note that you will need to edit the WorkingDirectory, EnvironmentFile, and ExecStart to the 
actual directory medna-metadata is in.*

Write and exit the VIM text editor:

```text
:wq!
```

### Enable the socket and service
```commandline
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

Check for the socket file (it should be green):

```commandline
sudo systemctl status gunicorn.socket
```

Check for the existence of the sock file:

```commandline
file /run/gunicorn.sock
```

If there is no file, check the socket's logs and troubleshoot:

```commandline
sudo journalctl -u gunicorn.socket
```

Test the socket activation (should be grey & inactive):

```commandline
sudo systemctl status gunicorn
```

Test the socket activation mechanism through curl:

```commandline
curl --unix-socket /run/gunicorn.sock localhost
```

Now see if Gunicorn is "running":

```commandline
sudo systemctl status gunicorn
```

If you need to troubleshoot, check `journalctl` and `daemon-reload` and `restart gunicorn` when the 
service, socket, settings, or env files are edited:

```commandline
sudo journalctl -u gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

### Configure Nginx

```commandline
sudo vim /etc/nginx/sites-available/medna-metadata
```


```text
server {
    listen 80;
    server_name your_ip_address yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/youruser/medna-metadata;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

*Please note that you will need to edit the server_name and location to the 
actual IP address or domain name and to the actual directory medna-metadata is in.*

Write and exit the VIM text editor:

```text
:wq!
```

Enable the file by linking it to sites-enabled:

```commandline
sudo ln -s /etc/nginx/sites-available/medna-metadata /etc/nginx/sites-enabled
```

Test the Nginx configuration for syntaix errors:
```commandline
sudo nginx -t
```

If there are no errors, restart Nginx:
```commandline
sudo systemctl restart nginx
```

Delete port 8000 and allow Nginx in the firewall:
```commandline
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```

### Troubleshooting Nginx and Gunicorn
* https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04

### SSL Certificates with Certbot 

```commandline
sudo certbot --nginx -d yourdomain.com
```

Follow the prompt by enter in your email address, [A], [n], and [2].

Verify Certbot auto-renewal
```commandline
sudo certbot renew --dry-run
```

### Collect Static
```commandline
workon mednaenv
```

*If you named your venv something other than `mednaenv`, use that here instead.*

Any time there is a change made to the python code, run the following:
```
git pull && python manage.py collectstatic --noinput --clear && sudo systemctl daemon-reload && sudo systemctl restart gunicorn.socket gunicorn.service
```

You should now be good to go and running with your desired server and domain.

## Docker Setup
*The modules in Maine-eDNA metadata have not yet been fully tested and migrated for the Dockerfile. 
This message will be updated after successful implementation with the following Docker commands.*

The `/docker` directory has `medna.env.db.txt`, `medna.env.txt`, and `nginx.proxycompanion.env.txt` which contain 
all environmental variables for docker deployment. Make a copy of these files with the `.txt` extension removed 
(e.g., `medna.env.db`, `medna.env`, `nginx.proxycompanion.env`) and variables updated with desired settings. 
These files are necessary for docker. Other files that affect docker are:
* `entrypoint.sh`
* `.dockerignore`
* contents of `/docker` directory
* settings in `medna_metadata/settings.py`


Once settings are verified, run `sudo docker-compose up -d` to build and deploy medna-metadata, PostgreSQL with PostGIS, 
and NGINX with LetsEncrypt.

