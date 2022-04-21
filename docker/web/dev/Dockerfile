# https://testdriven.io/courses/django-celery/docker/
# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
# https://testdriven.io/blog/deploying-django-to-digitalocean-with-docker-and-github-actions/
# https://www.digitalocean.com/community/tech_talks/deploying-to-digitalocean-with-github-actions
# pull official base image
FROM ubuntu:focal

# create directory for the django user
ENV HOME=/home/django
RUN mkdir -p $HOME

#RUN groupadd -r django && useradd -r -g django django
RUN adduser --disabled-password --gecos '' django
# create working directories
ENV VIRTUAL_ENV=$HOME/appenv
RUN mkdir -p $VIRTUAL_ENV
ENV APP_HOME=/home/django/medna-metadata
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media
RUN chown -R django:django $APP_HOME
WORKDIR $APP_HOME

# owner can read/write/execute, group/others can read/execute.
RUN chmod 755 -R $APP_HOME

# set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# switch to django user
USER django

# install dependencies
RUN pip install --upgrade pip

# Copy and install requirements
COPY --chown=django:django ./requirements ./requirements

# set permissions for docker-requirements.sh
# RUN chmod +x /home/django/requirements/docker-requirements.sh
RUN requirements/docker-requirements.sh

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade setuptools wheel
RUN pip install --no-cache-dir -r requirements/dev.txt

# copy app
COPY --chown=django:django . .

# Collect static files
RUN python manage.py collectstatic --noinput --clear
# RUN chmod +x entrypoint.sh

# set permissions for entrypoint.sh
RUN sed -i 's/\r$//g' /home/django/entrypoint.sh
# RUN chmod +x /home/django/entrypoint.sh

# set permissions for celeryworker celerybeat start
# COPY ./docker/celery/ .
RUN sed -i 's/\r$//g' /home/django/celerybeat_start.sh
RUN sed -i 's/\r$//g' /home/django/celeryworker_start.sh
# RUN chmod +x /home/django/celerybeat_start.sh
# RUN chmod +x /home/django/celeryworker_start.sh

# run entrypoint.sh
ENTRYPOINT ["/home/django/medna-metadata/entrypoint.sh"]
