###########
# BUILDER #
###########
# https://testdriven.io/courses/django-celery/docker/
# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
# https://testdriven.io/blog/deploying-django-to-digitalocean-with-docker-and-github-actions/
# https://github.com/testdrivenio/django-github-digitalocean/blob/master/.github/workflows/main.yml
# https://www.digitalocean.com/community/tech_talks/deploying-to-digitalocean-with-github-actions
# pull official base image
FROM ubuntu:focal as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy and install requirements
COPY ./requirements ./requirements

# set permissions for entrypoint.sh
RUN chmod +x requirements/docker-requirements.sh
RUN requirements/docker-requirements.sh

# lint
RUN pip install --upgrade pip
RUN pip install flake8==3.9.2
# copy project
COPY . .
RUN flake8 --ignore=E501,F401 .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements/prod.txt

#########
# FINAL #
#########
FROM ubuntu:focal

# create directory for the django user
ENV HOME=/home/django
RUN mkdir -p $HOME

#RUN groupadd -r django && useradd -r -g django django
RUN adduser --disabled-password --gecos '' django

# create the appropriate directories
ENV APP_HOME=/home/django/medna-metadata
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media
RUN chown -R django:django $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y libpq-dev python3-pip
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements/prod.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

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
RUN chown -R django:django $APP_HOME

# owner can read/write/execute, group/others can read/execute.
RUN chmod 755 -R $APP_HOME

# change to the app user
USER django

RUN chmod +x $APP_HOME/requirements/docker-requirements.sh
RUN $APP_HOME/requirements/docker-requirements.sh

# run entrypoint.sh
ENTRYPOINT ["/home/django/medna-metadata/entrypoint.sh"]
