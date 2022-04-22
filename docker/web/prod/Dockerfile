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
ENV VIRTUAL_ENV=$HOME/.virtualenvs/mednaenv
run mkdir -p $VIRTUAL_ENV

# create the appropriate directories
ENV APP_HOME=/home/django/medna-metadata
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media
RUN mkdir -p $APP_HOME/logs

RUN chown -R django:django $HOME

WORKDIR $APP_HOME

# Copy and install requirements
COPY ./requirements ./requirements

RUN chmod +x requirements/docker-requirements.sh
RUN requirements/docker-requirements.sh

  # cleaning up unused files
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN chown -R django:django $HOME
RUN chmod 755 -R $HOME

USER django

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade setuptools wheel
RUN pip install -r requirements/prod.txt

# Copy app
COPY . $APP_HOME

USER root

# set permissions for celeryworker celerybeat start
COPY ./docker/celery/ .
RUN sed -i 's/\r$//g' $APP_HOME/celerybeat_start.sh
RUN sed -i 's/\r$//g' $APP_HOME/celeryworker_start.sh
RUN chmod +x $APP_HOME/celerybeat_start.sh
RUN chmod +x $APP_HOME/celeryworker_start.sh

# set permissions for entrypoint.sh
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

# chown all the files to the app user
RUN chown -R django:django $HOME
# owner can read/write/execute, group/others can read/execute.
RUN chmod 755 -R $HOME

USER django
# run entrypoint.sh
ENTRYPOINT ["/home/django/medna-metadata/entrypoint.sh"]
