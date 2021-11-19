============
Installation
============

If you've never set up a server before, DigitalOcean provides an extensive variety of tutorials that we highly recommend:

 - https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04

The remaining steps were adapted from the following DigitalOcean tutorial:

 - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04

.. note::
    It's recommended to visit these tutorials to understand some of the rational behind the steps below.

.. _setup:
Setup
-----

The following instructions provide guidance on installing MeDNA-Metadata on Ubuntu 20.04.

Ubuntu (20.04 LTS is recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone the Repository
--------------------

To clone the most recent stable release as read-only::

    git clone -b latest https://github.com/Maine-eDNA/medna-metadata.git
    cd medna-metadata


To clone the development branch::

    git clone -b main git@github.com:Maine-eDNA/medna-metadata.git
    cd medna-metadata

Install Ubuntu Requirements::

   sudo bash /home/youruser/medna-metadata/requirementsubuntu-requirements.sh

It will run the following installation comands:

.. literalinclude:: ../../requirements/ubuntu-requirements.sh
   :language: bash

Create PostgreSQL database with PostGIS Extension
-------------------------------------------------

Create the database for your project::

   sudo -u postgres psql -c "CREATE DATABASE medna_metadata;"

Create a database user and add them to the project with a secure password::

    sudo -u postgres psql -c "CREATE USER django WITH PASSWORD 'your_db_password';"

Recommended settings from the Django project::

    sudo -u postgres psql -c "ALTER ROLE django SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE django SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE django SET timezone TO 'UTC';"

Set the Django user as the administrator for the medna_metadata database::

    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE medna_metadata TO django;"

Grant privledges to the Django database user to create databases for django tests::

    sudo -u postgres psql -c "ALTER USER django CREATEDB;"

Add PostGIS to medna_metadata::

    sudo -i -u postgres psql -d medna_metadata -c "CREATE EXTENSION postgis;"

Create a Virtual Environment and Set Environmental Variables
------------------------------------------------------------

Create a virtual environment with venv::

    sudo -H pip install --upgrade pip
    sudo -H pip install virtualenvwrapper
    sudo -H pip install virtualenv

Dotenv is a python library for reading in environmental variables from a file::

    pip install django-dotenv

Add environmental variables to the end of bashrc, which will reload the variables at restart.

The variables to copy into ``~/.bashrc`` are listed in ``docker/bashrc.txt``::

    sudo vim ~/.bashrc

.. note::
    to write and quit within the VIM text editor, ``[esc]``, ``:wq!``, and ``[enter]``

Load the environmental variables::

    source ~/.bashrc

Copy ``gunicorn.env.txt`` as ``gunicorn.env`` and modify the variables::

    cp docker/gunicorn.env.txt docker/gunicorn.env
    sudo vim docker/gunicorn.env

To create and activate virtualenvwrapper::

    mkvirtualenv --python /usr/bin/python3.8 mednaenv

.. note::
    Note that the version of python varies and you will have to check or install it.

 - https://stackoverflow.com/questions/6401951/using-different-versions-of-python-with-virtualenvwrapper
 - https://unix.stackexchange.com/questions/410579/change-the-python3-default-version-in-ubuntu

Activate the virtual environment::

    workon mednaenv

Install python requirements to the virtualenv::

    pip install -U -r /home/youruser/medna-metadata/requirements/prod.txt

Migrate the Database Tables
---------------------------

Migrate the database schema to PostgreSQL from within the same directory as ``manage.py``
Within each app there is a migration directory which contains files which tell the database how to
create the database tables. These have been pre-generated and added to this repository to simplify the
process of deplying the Maine-eDNA Metadata application::

    python manage.py migrate users
    python manage.py migrate utility
    python manage.py migrate field_sites
    python manage.py migrate sample_labels
    python manage.py migrate field_survey
    python manage.py migrate wet_lab
    python manage.py migrate freezer_inventory
    python manage.py migrate bioinfo_denoising
    python manage.py migrate bioinfo_taxon

Now, if everything looked good (e.g., no error messages), complete the remaining migrations::

    python manage.py migrate

Create a administrative user for the medna_metadata project
-----------------------------------------------------------

Create a superuser::

    python manage.py createsuperuser

When prompted, enter in your preferred credentials (email, password).

Collect all static content into the directory specified in settings.py
----------------------------------------------------------------------

Collect static files::

    python manage.py collectstatic

Test the deployment
-------------------

Temporarily create an exception for port 8000::

    sudo ufw allow 8000

Test the project deployment::

    python manage.py runserver 0.0.0.0:8000

In your web browser, visit the server's IP address followed by :8000

``http://youripaddress:8000``

Enter ``[CTRL-C]`` in to shut down the test deployment

Now test to see if the project can be deployed with Gunicorn::

    gunicorn --bind 0.0.0.0:8000 medna-metadata.wsgi

If you were able to visit the same page while deployed with Gunicorn, continue onward. If not, some helpful
troubleshooting steps can be found in the DigitalOcean tutorial on setting up Django with PostgreSQL, Gunicorn, and Nginx:
 - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04

Create `Gunicorn <https://gunicorn.org/>`_ Socket and Service files (e.g., daemonizing!)
----------------------------------------------------------------------------------------

Leave the virtualenv::

    deactivate

Create a systemd Socket file::

    sudo vim /etc/systemd/system/gunicorn.socket

Write the following to the file::

    [Unit]
    Description=gunicorn socket

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target

Write and exit the VIM text editor::

    :wq!

Create a systemd service file::

    sudo vim /etc/systemd/system/gunicorn.service

Modify then write the following to the file::

    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target

    [Service]
    User=youruser
    Group=youruser
    WorkingDirectory=/home/youruser/medna-metadata
    EnvironmentFile=/home/youruser/medna-metadata/docker/gunicorn.env
    ExecStart=/home/youruser/.virtualenvs/mednaenv/bin/gunicorn \
              --access-logfile - --workers 3 \
              --bind unix:/run/gunicorn.sock \
              medna_metadata.wsgi:application

    [Install]
    WantedBy=multi-user.target

.. note::
    You will need to replace the ``User`` and ``Group`` to the correct Ubuntu username and group and modify the
    ``WorkingDirectory``, ``EnvironmentFile``, and ``ExecStart`` to the actual directory medna-metadata is in.

Write and exit the VIM text editor::

    :wq!

Enable the socket and service::

    sudo systemctl start gunicorn.socket
    sudo systemctl enable gunicorn.socket

Check for the socket file's status (it should be green)::

    sudo systemctl status gunicorn.socket

Check for the existence of the sock file::

    file /run/gunicorn.sock

If there is no file, check the socket's logs and troubleshoot::

    sudo journalctl -u gunicorn.socket

Test the socket activation (should be grey & inactive)::

    sudo systemctl status gunicorn

Test the socket activation mechanism through curl::

    curl --unix-socket /run/gunicorn.sock localhost

Now see if Gunicorn is "running"::

    sudo systemctl status gunicorn

If you need to troubleshoot, check ``journalctl`` and ``daemon-reload`` and ``restart gunicorn`` when the
service, socket, settings, or env files are edited::

    sudo journalctl -u gunicorn
    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn

Setup `Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`_ and `RabbitMQ <https://www.rabbitmq.com/>`_
-----------------------------------------------------------------------------------------------------------------------------------------

Celery task management and the RabbitMQ messaging server are used for task queues within the backend application. This
allows for things such as queues of data transformations and workers that will spawn as resources are available.

 - https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#first-steps
 - https://www.digitalocean.com/community/tutorials/how-to-use-celery-with-rabbitmq-to-queue-tasks-on-an-ubuntu-vps
 - https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html

.. note::
    Celery and Rabbitmq should have already been installed with the requirements.txt and ubuntu-requirements.sh, but the commands are also provided here.

Install rabbitmq messaging server::

    sudo apt-get update
    sudo apt-get install rabbitmq-server

.. note::
    If you named your venv something other than ``mednaenv``, use that here instead.

Activate the virtualenv::

    workon mednaenv

Install  Celery::

    pip install celery==4.4.7

Configure RabbitMQ
~~~~~~~~~~~~~~~~~~

Add a user and a virtual host::

    sudo rabbitmqctl add_user youruser yourpassword
    sudo rabbitmqctl add_vhost mednadatavhost
    sudo rabbitmqctl set_user_tags youruser mednatag
    sudo rabbitmqctl set_permissions -p mednadatavhost youruser ".*" ".*" ".*"

Stop rabbitmq::

    sudo systemctl stop rabbitmq-server

Check to verify it is actually stopped::

    sudo rabbitmqctl cluster_status

Start it up again::

    sudo systemctl start rabbitmq-server
    sudo systemctl restart rabbitmq-server
    sudo systemctl status rabbitmq-server

.. note::
    For Celery and RabbitMQ to function, the ``CELERY_RESULT_BACKEND`` and ``CELERY_BROKER_URL`` variables must be set in ``~/.bashrc``
    and ``docker/gunicorn.env``. These variables should resemble the following:
     - CELERY_RESULT_BACKEND='rpc'
     - CELERY_BROKER_URL='pyamqp://youruser:yourpassword@localhost:5672/mednadatavhost`

Create `Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`_ Worker and Beat files (e.g., daemonizing!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like gunicorn, the celery worker processes should be run as a Systemd service.

Create a celeryworker service file::

    sudo vim /etc/systemd/system/celeryworker.service

Modify then write the following to the file::

    [Unit]
    Description=celeryworker daemon
    After=network.target

    [Service]
    User=youruser
    Group=youruser
    WorkingDirectory=/home/youruser/medna-metadata
    Environment=DJANGO_SETTINGS_MODULE=medna_metadata.settings
    ExecStart=/home/youruser/.virtualenvs/mednaenv/bin/celery worker \
      -A medna_metadata.celery.app \
      -c 2 -Q celery,default -n "allqueues.%%h"

    [Install]
    WantedBy=multi-user.target

Write and exit the VIM text editor::

    :wq!

.. note::
    You will need to replace the ``User`` and ``Group`` to the correct Ubuntu username and group and modify the
    ``WorkingDirectory`` and ``ExecStart`` to the actual directory medna-metadata is in.


We also need a celery beat Systemd service for scheduling tasks.

Create a celeryworker beat file::

    sudo vim /etc/systemd/system/celerybeat.service

Modify then write the following to the file::

    [Unit]
    Description=celerybeat daemon
    After=network.target

    [Service]
    User=youruser
    Group=youruser
    WorkingDirectory=/home/youruser/medna-metadata
    Environment=DJANGO_SETTINGS_MODULE=medna_metadata.settings
    ExecStart=/home/youruser/.virtualenvs/mednaenv/bin/celery beat \
      -A medna_metadata.celery.app --loglevel INFO

    [Install]
    WantedBy=multi-user.target

Write and exit the VIM text editor::

    :wq!

.. note::
    You will need to replace the ``User`` and ``Group`` to the correct Ubuntu username and group and modify the
    ``WorkingDirectory`` and ``ExecStart`` to the actual directory medna-metadata is in.

We can now start the celeryworker and celerybeat services::

    sudo systemctl start celeryworker
    sudo systemctl status celeryworker

    sudo systemctl start celerybeat
    sudo systemctl status celerybeat

If any modifications are made to any ``tasks.py`` or ``medna_metadata/celery.py``, restart ``celerybeat`` and ``celeryworker``::

    sudo systemctl restart celerybeat && sudo systemctl restart celeryworker && sudo systemctl daemon-reload && sudo systemctl restart gunicorn

If you want these services to start automatically on boot, you can enable them as follows::

    sudo systemctl enable celeryworker
    sudo systemctl enable celerybeat

Troubleshooting Celery
~~~~~~~~~~~~~~~~~~~~~~

If you are trying to troubleshoot celerybeat or celeryworker, be sure to check system logs for error messages::

    sudo cat /var/log/syslog
    sudo tail /var/log/syslog -n 40

You can also check RabbitMQ logs::

    sudo tail /var/log/rabbitmq/rabbit@medna-metadata.log -n 50

To view Celery tasks as they are sent by RabbitMQ::

    celery worker -A medna_metadata --pool=solo -l info

``[CTRL-C]`` to exit.

Collect Static Files
--------------------

Any time there is a change made to the python code, run the following to reload changes::

    git pull && python manage.py collectstatic --noinput --clear && sudo systemctl daemon-reload && sudo systemctl restart gunicorn.socket gunicorn.service

Configure `Nginx <https://www.nginx.com/>`_
-------------------------------------------

Create a nginx config file::

    sudo vim /etc/nginx/sites-available/medna-metadata

Modify and write the following::

    server {
        listen 80;
        server_name youripaddress yourdomain.com;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /home/youruser/medna-metadata;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }

.. note::
    You will need to edit the ``server_name`` and ``location`` to the actual IP address or domain name and to the actual directory medna-metadata is in.

Write and exit the VIM text editor::

    :wq!

Enable the file by linking it to sites-enabled::

    sudo ln -s /etc/nginx/sites-available/medna-metadata /etc/nginx/sites-enabled

Test the Nginx configuration for syntaix errors::

    sudo nginx -t

If there are no errors, restart Nginx::

    sudo systemctl restart nginx

Delete port 8000 and allow Nginx in the firewall::

    sudo ufw delete allow 8000
    sudo ufw allow 'Nginx Full'

Troubleshooting Nginx and Gunicorn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For more information on troubleshooting Nginx and Gunicorn, please see the following:
 - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04

SSL Certificates with Certbot
-----------------------------

Run certbot::

    sudo certbot --nginx -d yourdomain.com

Follow the prompt by enter in your ``email address``, ``[A]``, ``[n]``, and ``[2]``.

Verify Certbot auto-renewal::

    sudo certbot renew --dry-run

You should now be good to go and running with your desired server and domain.

Docker Setup
------------
.. note::
    The modules in Maine-eDNA metadata have not yet been fully tested and migrated for the Dockerfile. 
    This message will be updated after successful implementation with the following Docker commands.

The ``/docker`` directory has ``medna.env.db.txt``, ``medna.env.txt``, and ``nginx.proxycompanion.env.txt`` which contain
all environmental variables for docker deployment. Make a copy of these files with the ``.txt`` extension removed
(e.g., ``medna.env.db``, ``medna.env``, ``nginx.proxycompanion.env``) and variables updated with desired settings.
These files are necessary for docker. Other files that affect docker are:
 - ``entrypoint.sh``
 - ``.dockerignore``
 - contents of ``/docker`` directory
 - settings in ``medna_metadata/settings.py``


Once settings are verified, run ``sudo docker-compose up -d`` to build and deploy medna-metadata, PostgreSQL with PostGIS,
and NGINX with LetsEncrypt.
