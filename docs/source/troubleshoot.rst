===============
Troubleshooting
===============

When determining the source of an issue, there are a handful of avenues one can take while troubleshooting. The following
are the most common and accessible options in Django.

DEBUG Mode
----------
Django provides a `DEBUG mode <https://docs.djangoproject.com/en/4.0/ref/settings/#debug>`__, where errors are displayed directly in the frontend (user facing web content) while browsing.
This is helpful in that a developer is provided with the source of an error rather than a generic failure page. However,
DEBUG mode consumes a significant amount of resources and the outputs publicly display secure information. It is not advised
to use DEBUG mode on a production (live) server.

Within medna-metadata, Django's ``DEBUG`` mode can be toggled on (True) or off (False) through the ``DJANGO_DEBUG`` environmental
setting. For manual installations of medna-metadata, this setting will be set in ``bashrc`` and ``docker/gunicorn.env``.
For a docker-compose installation, this setting will be set in ``docker/medna.env``.

Logging
-------
Another common method to find the source of an issue that is separate from ``DEBUG`` mode, is through log files.
medna-metadata stores logs in a few locations:

* Django logs - ``/tmp/``
* Gunicorn access and error logs - ``/tmp/``
* Celery beat and worker logs - ``/var/log/celery/``
* PostgreSQL logs - ``/var/log/postgresql/``
* NGINX logs - ``/var/log/nginx/``
* RabbitMQ logs - ``/var/log/rabbitmq/``

Manual Installation Logs
~~~~~~~~~~~~~~~~~~~~~~~~
If services were daemonized during a manual installation, additional information may be available through system status and logs::

    # show daemonization status - this shows if a service is running
    sudo systemctl status gunicorn
    sudo systemctl status nginx
    sudo systemctl status celery.service
    sudo systemctl status celerybeat.service

    # show journal entries for each service
    sudo journalctl -u gunicorn
    sudo journalctl -u nginx
    sudo journalctl -u celery.service
    sudo journalctl -u celerybeat.service

    # print system logs
    sudo cat /var/log/syslog
    sudo tail /var/log/syslog -n 40

Docker-Compose Installation Logs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For a docker-compose installation, log file directories are accessible after entering a docker container. To enter the medna-metadata docker container, use the following command::

    sudo docker exec -it medna_metadata_web /bin/bash

To exit the docker container::

    exit

