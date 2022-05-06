============
Installation
============

.. important::
    Ubuntu (20.04 LTS is recommended)

.. seealso::
    If you've never set up a server before, DigitalOcean provides an extensive variety of tutorials that we highly recommend.
    Several of the steps below were adapted from their tutorials.
     - `Initial Server Setup With Ubuntu 20.04 <https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04>`__
     - `Django, PostgreSQL, NGINX, Gunicorn, and Ubuntu 20.04 <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04>`__
    It's recommended to visit these tutorials to understand some of the rational behind the steps below.

The following instructions provide guidance on installing MeDNA-Metadata on Ubuntu 20.04.

.. important::
    Instances of ``youruser`` need to be replaced with a relevant username. For example, references to ``/home/youruser/``
    must be adjusted to the active Ubuntu username. The simplest solution would be to use the same username throughout the
    setup process, as long as it is **not** the root username. Never use root. For more information, see the aforementioned
    `Initial Server Setup With Ubuntu 20.04 <https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04>`__.

====================
Clone the Repository
====================

To clone the most recent stable release as read-only::

    git clone -b stable/1.0.x https://github.com/Maine-eDNA/medna-metadata.git

To clone the development branch::

    git clone -b main git@github.com:Maine-eDNA/medna-metadata.git

============
Docker Setup
============

Install Requirements
--------------------

Ubuntu 20.04
~~~~~~~~~~~~
Deploying with docker requires docker and docker-compose. Docker-compose must be able to run at least version 3.8.
DigitalOcean provides tutorials on `How to Install and Use Docker on Ubuntu 20.04 <https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04>`__
and `How To Install and Use Docker Compose on Ubuntu 20.04 <https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04>`__.

After following DigitalOcean's tutorials, create a symbolic link of the installation to the ``docker-compose`` command ::

    sudo ln -s ~/.docker/cli-plugins/docker-compose /usr/bin/docker-compose

.. important::
    This allows you to call ``docker-compose`` from the command line, and is highly recommended to avoid future headaches.

The ``/docker`` directory has ``medna.env.txt`` and ``medna.env.db.txt``, which contain all environmental variables for
docker deployment. These files are necessary for docker. Other files that affect docker are:
 - ``entrypoint.sh``
 - ``.dockerignore``
 - contents of ``/docker`` directory
 - settings in ``medna_metadata/settings.py``

Navigate to the ``/docker`` directory ::

    cd medna-metadata/docker/

Make a copy of ``medna.env.txt`` and ``medna.env.db.txt`` in the same ``/docker`` directory with the ``.txt`` extension removed (e.g., ``medna.env.db``, ``medna.env``) ::

    cp medna.env.txt medna.env
    cp medna.env.db.txt medna.env.db

``medna.env``:

.. literalinclude:: ../../docker/medna.env.txt
   :language: env

``medna.env.db``:

.. literalinclude:: ../../docker/medna.env.db.txt
   :language: env

Open and update the environmental variables with desired settings in a text editor such as VIM ::

    sudo vim medna.env

Write and exit the VIM text editor::

    :wq!

Repeat these steps with ``medna.env.db``.

Once settings are verified, run ``sudo docker-compose up -d`` from the ``/docker`` directory to build and deploy Maine-eDNA Metadata,
`PostgreSQL with PostGIS <https://registry.hub.docker.com/r/postgis/postgis/>`__, `RabbitMQ <https://hub.docker.com/_/rabbitmq>`__,
`Celery <https://docs.celeryq.dev/en/stable/userguide/configuration.html>`__, `Gunicorn <https://gunicorn.org/>`__, and
`NGINX <https://hub.docker.com/_/nginx>`__.

After the containers are up, it will take a moment for the application to set itself up. Once it is done, it will be
accessible at `http://localhost:8000`

============
Manual Setup
============

Install Requirements
--------------------

Ubuntu 20.04
~~~~~~~~~~~~

Install Ubuntu Requirements::

   cd medna-metadata
   sudo bash requirements/ubuntu-requirements.sh

It will run the following installation commands:

.. literalinclude:: ../../requirements/ubuntu-requirements.sh
   :language: bash

Create a Virtual Environment and Set Environmental Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a virtual environment with venv::

    sudo -H pip install --upgrade pip
    sudo -H pip install virtualenvwrapper
    sudo -H pip install virtualenv

Dotenv is a python library for reading in environmental variables from a file::

    pip install django-dotenv

Add environmental variables to the bottom of bashrc, which reloads environmental variables anytime the server reboots.

The environmental variables required to run this application are listed in ``docker/bashrc.txt``:

.. literalinclude:: ../../docker/bashrc.txt
   :language: env

These environmental variables must be updated with values specific to your deployment.

Open ``~/.bashrc`` with a text editor such as VIM::

    sudo vim ~/.bashrc

Scroll to the bottom of ``bashrc`` and type ``i`` to insert into the file. Write and exit the VIM text editor::

    :wq!

.. tip::
    To write and quit within the VIM text editor, ``[esc]``, ``:wq!``, and ``[enter]``

Load the environmental variables::

    source ~/.bashrc

Make a copy of ``gunicorn.env.txt`` in the same ``/docker`` directory with the ``.txt`` extension removed (e.g., ``gunicorn.env``) ::

    cp docker/gunicorn.env.txt docker/gunicorn.env

``gunicorn.env``:

.. literalinclude:: ../../docker/gunicorn.env.txt
   :language: env

Update the environmental variables with values specific to your deployment in a text editor such as VIM ::

    sudo vim docker/gunicorn.env

Type ``i`` to insert into the file. Write and exit the VIM text editor::

    :wq!

.. warning::
    MeDNA-Metadata **will not** successfully deploy without setting these environmental variables.

Create and activate virtualenvwrapper::

    mkvirtualenv --python /usr/bin/python3.8 mednaenv

.. important::
    The version of python varies and you will have to check or install it.
     - `Python with Virtualenvwrapper <https://stackoverflow.com/questions/6401951/using-different-versions-of-python-with-virtualenvwrapper>`__
     - `Change Ubuntu's Default Python Version <https://unix.stackexchange.com/questions/410579/change-the-python3-default-version-in-ubuntu>`__

Activate the virtual environment::

    workon mednaenv

Install python requirements to the virtualenv::

    pip install -U -r requirements/prod.txt

The following python libraries will install:
.. literalinclude:: ../../requirements/base.txt
   :language: env
.. literalinclude:: ../../requirements/prod.txt
   :language: env

Create `PostgreSQL <https://www.postgresql.org/>`__ database with `PostGIS <https://postgis.net/>`__ Extension
--------------------------------------------------------------------------------------------------------------

Create the database for your project::

   sudo -u postgres psql -c "CREATE DATABASE medna_metadata;"

Create a database user and add them to the project with a secure password::

    sudo -u postgres psql -c "CREATE USER youruser WITH PASSWORD 'yourdbpassword';"

Recommended settings from the `Django <https://www.djangoproject.com/>`__ project::

    sudo -u postgres psql -c "ALTER ROLE youruser SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE youruser SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE youruser SET timezone TO 'UTC';"

Set ``youruser`` as the administrator for the medna_metadata database::

    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE medna_metadata TO youruser;"

Grant privileges to the ``youruser`` database user to create databases for `Django <https://www.djangoproject.com/>`__ tests::

    sudo -u postgres psql -c "ALTER USER youruser CREATEDB NOSUPERUSER NOCREATEROLE;"

Add the `PostGIS <https://postgis.net/>`__ extension to medna_metadata::

    sudo -i -u postgres psql -d medna_metadata -c "CREATE EXTENSION postgis;"

.. tip::
    It would be advantageous here to use the same username as your selected Ubuntu username.

Migrate the Database Tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Migrate the database schema to `PostgreSQL <https://www.postgresql.org/>`__ from within the same directory as ``manage.py``
Within each app there is a migration directory which contains files which tell the database how to
create the database tables. These have been pre-generated and added to this repository to simplify the
process of deplying the Maine-eDNA Metadata application::

    python manage.py migrate users
    python manage.py migrate utility
    python manage.py migrate field_site
    python manage.py migrate sample_label
    python manage.py migrate field_survey
    python manage.py migrate wet_lab
    python manage.py migrate freezer_inventory
    python manage.py migrate bioinfo

Now, if everything looked good (e.g., no error messages), complete the remaining migrations::

    python manage.py migrate

Create Superuser
----------------

Creating a ``superuser`` adds an administrative user with full privileges to the MeDNA-Metadata project.

Create a superuser::

    python manage.py createsuperuser

When prompted, enter in your preferred credentials (``youremail``, ``yourpassword``).

Collect Static
--------------

Collecting static files will copy all static content into the directory specified in ``settings.py``.

Collect static files::

    python manage.py collectstatic

Test The Deployment
-------------------

Temporarily create an exception for port 8000::

    sudo ufw allow 8000

Test the project deployment::

    python manage.py runserver 0.0.0.0:8000

In your web browser, visit the server's IP address followed by :8000

``http://youripaddress:8000``

If you're able to see a live project, then enter ``[CTRL-C]`` in to shut down the test deployment.

Test Gunicorn
~~~~~~~~~~~~~

Now test to see if the project can be deployed with `Gunicorn <https://gunicorn.org/>`__::

    gunicorn --bind 0.0.0.0:8000 medna_metadata.wsgi

.. seealso::
    If you were able to visit the same page while deployed with `Gunicorn <https://gunicorn.org/>`__, continue onward. If not, some helpful
    troubleshooting steps can be found in the DigitalOcean tutorial on setting up `Django <https://www.djangoproject.com/>`__
    with `PostgreSQL <https://www.postgresql.org/>`__, `Gunicorn <https://gunicorn.org/>`__, and `Nginx <https://www.nginx.com/>`__.
     - `Django with PostgreSQL, Gunicorn, and Nginx on Ubuntu 20.04 <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04>`__

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
    WorkingDirectory=/path/to/medna-metadata
    EnvironmentFile=/path/to/medna-metadata/docker/gunicorn.env
    ExecStart=/path/to/.virtualenvs/mednaenv/bin/gunicorn \
              --access-logfile - --workers 3 \
              --bind unix:/run/gunicorn.sock \
              medna_metadata.wsgi:application

    [Install]
    WantedBy=multi-user.target

.. warning::
    You will need to replace the ``User`` and ``Group`` to the correct Ubuntu username and group and modify the
    ``WorkingDirectory``, ``EnvironmentFile``, and ``ExecStart`` to the actual directory MeDNA-Metadata is in.

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

Now see if `Gunicorn <https://gunicorn.org/>`__ is "running"::

    sudo systemctl status gunicorn

If you need to troubleshoot, check ``journalctl`` and ``daemon-reload`` and ``restart gunicorn`` when the
service, socket, settings, or env files are edited::

    sudo journalctl -u gunicorn
    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn

Setup `Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`__ and `RabbitMQ <https://www.rabbitmq.com/>`__
-------------------------------------------------------------------------------------------------------------------------------------------

`Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`__ task management and the
`RabbitMQ <https://www.rabbitmq.com/>`__
messaging server are used for task queues within the backend application. This allows for things such as queues of data
transformations and workers that will spawn as resources are available.

.. seealso::
    - `Celery First Steps <https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#first-steps>`__
    - `Celery, RabbitMQ, and Ubuntu <https://www.digitalocean.com/community/tutorials/how-to-use-celery-with-rabbitmq-to-queue-tasks-on-an-ubuntu-vps>`__
    - `Celery and Django <https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html>`__

.. note::
    `Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`__ and
    `RabbitMQ <https://www.rabbitmq.com/>`__ should have already been installed with the requirements.txt and
    ubuntu-requirements.sh, but the commands are also provided here.

Install `RabbitMQ <https://www.rabbitmq.com/>`__ messaging server::

    sudo apt-get update
    sudo apt-get install rabbitmq-server

.. important::
    If you named your venv something other than ``mednaenv``, use that here instead.

Activate the virtualenv::

    workon mednaenv

Install `Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`__::

    pip install -U "celery>=5.2.3"

Setup `RabbitMQ <https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/rabbitmq.html#setting-up-rabbitmq>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a user and a virtual host::

    sudo rabbitmqctl add_user youruser yourpassword
    sudo rabbitmqctl add_vhost yourvhost
    sudo rabbitmqctl set_user_tags youruser yourtag
    sudo rabbitmqctl set_permissions -p yourvhost youruser ".*" ".*" ".*"

.. warning::
    You will need to replace ``youruser``, ``yourpassword``, ``yourvhost``, ``yourtag``, to the password, username, tag
    and hostname of your choosing. These are specific to RabbitMQ and not dependent on other applications. What is
    chosen is used to construct your `CELERY_BROKER_URL <https://docs.celeryproject.org/en/stable/userguide/configuration.html#broker-settings>`__.

Stop `RabbitMQ <https://www.rabbitmq.com/>`__::

    sudo systemctl stop rabbitmq-server

Check to verify it is actually stopped::

    sudo rabbitmqctl cluster_status

Start it up again::

    sudo systemctl start rabbitmq-server
    sudo systemctl restart rabbitmq-server
    sudo systemctl status rabbitmq-server

.. warning::
    For `Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`__ and
    `RabbitMQ <https://www.rabbitmq.com/>`__ to function, the `CELERY_RESULT_BACKEND <https://docs.celeryproject.org/en/stable/userguide/configuration.html#result-backend>`__
    and `CELERY_BROKER_URL <https://docs.celeryproject.org/en/stable/userguide/configuration.html#broker-settings>`__
    variables must be set in ``~/.bashrc`` and ``docker/gunicorn.env``. These variables should resemble the following:
     - CELERY_RESULT_BACKEND='rpc'
     - CELERY_BROKER_URL='pyamqp://youruser:yourpassword@localhost:port/yourvhost`

Create `Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`__ Worker and Beat files (e.g., daemonizing!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like Gunicorn, `celery should be run as a Systemd service <https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#usage-systemd>`__.
--

First, open your environment file::

    sudo vim docker/gunicorn.env

Update or add the following `Celery config settings <https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#generic-systemd-celery-example>`__ to your environment file::

    CELERY_RESULT_BACKEND='your_result_backend'
    CELERY_BROKER_URL='transport://your_rabbitmq_user:your_rabbitmq_password@hostname:port/your_rabbitmq_vhost'
    CELERYD_NODES='worker'
    CELERY_BIN='/path/to/.virtualenvs/mednaenv/bin/celery'
    CELERY_APP='medna_metadata.celery.app'
    CELERYD_MULTI='multi'
    CELERYD_OPTS=''
    CELERYD_PID_FILE='/var/run/celery/%n.pid'
    CELERYD_LOG_FILE='/var/log/celery/%n%I.log'
    CELERYD_LOG_LEVEL='INFO'
    CELERYBEAT_PID_FILE='/var/run/celery/beat.pid'
    CELERYBEAT_LOG_FILE='/var/log/celery/beat.log'

Write and exit the VIM text editor::

    :wq!

Now we need to create the Celery log and run directories and update their permissions::

    sudo mkdir /var/run/celery/
    sudo mkdir /var/log/celery/

    sudo chgrp yourgroup /var/run/celery/
    sudo chgrp yourgroup /var/log/celery/

    sudo chmod g+rwx /var/run/celery/
    sudo chmod g+rwx /var/log/celery/

Create a `Celery service file <https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#service-file-celery-service>`__::

    sudo vim /etc/systemd/system/celery.service

Modify then write the following to the file::

    [Unit]
    Description=Celery Service
    After=network.target rabbitmq-server.service
    Requires=rabbitmq-server.service

    [Service]
    Type=forking
    User=youruser
    Group=yourgroup
    EnvironmentFile=/path/to/medna-metadata/docker/gunicorn.env
    WorkingDirectory=/path/to/medna-metadata
    Environment=DJANGO_SETTINGS_MODULE=medna_metadata.settings
    ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} multi start ${CELERYD_NODES} \
        --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
        --loglevel="${CELERYD_LOG_LEVEL}" ${CELERYD_OPTS}'
    ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
        --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
        --loglevel="${CELERYD_LOG_LEVEL}"'
    ExecReload=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} multi restart ${CELERYD_NODES} \
        --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
        --loglevel="${CELERYD_LOG_LEVEL}" ${CELERYD_OPTS}'
    Restart=always

    [Install]
    WantedBy=multi-user.target

Write and exit the VIM text editor::

    :wq!

.. warning::
    You will need to replace the ``User`` and ``Group`` to the correct Ubuntu username and group and modify the
    ``WorkingDirectory`` and ``EnvironmentFile`` to the actual directory MeDNA-Metadata is in.

We also need a `celerybeat Systemd service <https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#service-file-celerybeat-service>`__ for scheduling tasks.

Create a `celerybeat file <https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#service-file-celerybeat-service>`__::

    sudo vim /etc/systemd/system/celerybeat.service

Modify then write the following to the file::

    [Unit]
    Description=Celery Beat Service
    After=network.target rabbitmq-server.service
    Requires=rabbitmq-server.service

    [Service]
    Type=simple
    User=youruser
    Group=yourgroup
    EnvironmentFile=/path/to/medna-metadata/docker/gunicorn.env
    WorkingDirectory=/path/to/medna-metadata
    Environment=DJANGO_SETTINGS_MODULE=medna_metadata.settings
    ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat  \
        --pidfile=${CELERYBEAT_PID_FILE} \
        --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'
    Restart=always

    [Install]
    WantedBy=multi-user.target

Write and exit the VIM text editor::

    :wq!

.. warning::
    You **must** replace the ``User`` and ``Group`` to the correct Ubuntu username and group and modify the
    ``WorkingDirectory`` and ``EnvironmentFile`` to the actual directory MeDNA-Metadata is in.

We can now start the celery and celerybeat services::

    sudo systemctl daemon-reload
    sudo systemctl start celery.service
    sudo systemctl status celery.service

    sudo systemctl start celerybeat.service
    sudo systemctl status celerybeat.service

If any modifications are made to any ``tasks.py`` or ``medna_metadata/celery.py``, restart ``celerybeat`` and ``celeryworker``::

    sudo systemctl restart celery.service && sudo systemctl restart celerybeat.service && sudo systemctl daemon-reload && sudo systemctl restart gunicorn

If you want these services to start automatically on boot, you can enable them as follows::

    sudo systemctl enable celery.service
    sudo systemctl enable celerybeat.service

Troubleshooting `Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are trying to troubleshoot celery or celerybeat, be sure to check system logs for error messages::

    sudo cat /var/log/syslog
    sudo tail /var/log/syslog -n 40

You can also check `RabbitMQ <https://www.rabbitmq.com/>`__ logs::

    sudo tail /var/log/rabbitmq/rabbit@medna-metadata.log -n 50

To view `Celery <https://docs.celeryproject.org/en/stable/getting-started/introduction.html/>`__ tasks as they are sent by `RabbitMQ <https://www.rabbitmq.com/>`__::

    celery -A medna_metadata worker --pool=solo -l info

``[CTRL-C]`` to exit.

Collect Static Files
--------------------

Any time there is a change made to the python code, run the following to reload changes::

    git pull && python manage.py collectstatic --noinput --clear && sudo systemctl daemon-reload && sudo systemctl restart gunicorn.socket gunicorn.service

Configure `Nginx <https://www.nginx.com/>`__
--------------------------------------------

Create a nginx config file::

    sudo vim /etc/nginx/sites-available/medna-metadata

Modify and write the following::

    server {
        listen 80;
        server_name youripaddress yourdomain.com;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /path/to/medna-metadata;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_connect_timeout 300s;
            proxy_read_timeout 300s;
        }
    }

.. warning::
    You **must** edit the ``server_name`` and ``location`` to the actual IP address or domain name and to the actual directory MeDNA-Metadata is in.

Write and exit the VIM text editor::

    :wq!

Enable the file by linking it to sites-enabled::

    sudo ln -s /etc/nginx/sites-available/medna-metadata /etc/nginx/sites-enabled

Test the `Nginx <https://www.nginx.com/>`__ configuration for syntaix errors::

    sudo nginx -t

If there are no errors, restart `Nginx <https://www.nginx.com/>`__::

    sudo systemctl restart nginx

Delete port 8000 and allow `Nginx <https://www.nginx.com/>`__ in the firewall::

    sudo ufw delete allow 8000
    sudo ufw allow 'Nginx Full'

Troubleshooting `Nginx <https://www.nginx.com/>`__ and `Gunicorn <https://gunicorn.org/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. seealso::
    For more information on troubleshooting `Nginx <https://www.nginx.com/>`__ and `Gunicorn <https://gunicorn.org/>`__, please see the following:
     - `Django with PostgreSQL, NGINX, and Gunicorn on Ubuntu 20.04 <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04>`__

SSL Certificates with Certbot
-----------------------------

Run certbot::

    sudo certbot --nginx -d yourdomain.com

Follow the prompt by enter in your ``email address``, ``[A]``, ``[n]``, and ``[2]``.

Verify Certbot auto-renewal::

    sudo certbot renew --dry-run

You should now be good to go and running with your desired server and domain.