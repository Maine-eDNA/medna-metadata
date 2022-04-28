# pull official base image
FROM ubuntu:focal

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#RUN groupadd -r django && useradd -r -g django django
RUN adduser --disabled-password --gecos '' django

# create directory for the django user
ENV HOME=/home/django
RUN mkdir -p $HOME

# create the appropriate directories
ENV APP_HOME=/home/django/medna-metadata
RUN mkdir -p $APP_HOME

RUN chown -R django:django $HOME

WORKDIR $APP_HOME

# Copy and install requirements
COPY ./requirements ./requirements

RUN chmod +x requirements/docker-requirements.sh
RUN requirements/docker-requirements.sh

 # clean up unused files
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && rm -rf /var/lib/apt/lists/*

# link python3 to python so that 'python' cmd calls python3
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN chown -R django:django $HOME
RUN chmod 755 -R $HOME

USER django

# create venv dir and activate the venv
ENV VIRTUAL_ENV=$HOME/.virtualenvs/mednaenv
RUN mkdir -p $VIRTUAL_ENV
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade setuptools wheel
RUN pip install -r requirements/prod.txt

# Copy app
COPY . $APP_HOME

USER root

# set permissions for celeryworker celerybeat start
COPY ./docker/celery/ $HOME
RUN sed -i 's/\r$//g' $HOME/celerybeat_start.sh
RUN sed -i 's/\r$//g' $HOME/celeryworker_start.sh
RUN chmod +x $HOME/celerybeat_start.sh
RUN chmod +x $HOME/celeryworker_start.sh

# create log dirs for celery with appropriate permissions
RUN mkdir /var/run/celery/
RUN mkdir /var/log/celery/
RUN chgrp django /var/run/celery/
RUN chgrp django /var/log/celery/
RUN chmod g+rwx /var/run/celery/
RUN chmod g+rwx /var/log/celery/

# set permissions for entrypoint.sh
COPY ./entrypoint.sh $HOME/entrypoint.sh
RUN sed -i 's/\r$//g' $HOME/entrypoint.sh
RUN chmod +x $HOME/entrypoint.sh

# set permissions for entrypoint.sh
COPY ./docker/web/web_start.sh $HOME/web_start.sh
RUN sed -i 's/\r$//g' $HOME/web_start.sh
RUN chmod +x $HOME/web_start.sh

# chown all the files to the app user
RUN chown -R django:django $HOME
# owner can read/write/execute, group/others can read/execute.
RUN chmod 755 -R $HOME

USER django
# run entrypoint.sh
ENTRYPOINT ["/home/django/entrypoint.sh"]
