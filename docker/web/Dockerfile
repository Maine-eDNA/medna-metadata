# https://testdriven.io/courses/django-celery/docker/
# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
# https://testdriven.io/blog/deploying-django-to-digitalocean-with-docker-and-github-actions/
# https://www.digitalocean.com/community/tech_talks/deploying-to-digitalocean-with-github-actions
# pull official base image
FROM ubuntu:focal

# set work directory
WORKDIR /usr/src/app

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

# install dependencies
RUN pip install --upgrade pip

# Copy and install requirements
COPY ./requirements ./requirements

# set permissions for docker-requirements.sh
RUN chmod +x /usr/src/app/requirements/docker-requirements.sh
RUN requirements/docker-requirements.sh

RUN pip install -r requirements/dev.txt

# copy project
COPY . .

# set permissions for entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# set permissions for celeryworker celerybeat start
COPY ./docker/celery/ .
RUN sed -i 's/\r$//g' /usr/src/app/celerybeat_start.sh
RUN sed -i 's/\r$//g' /usr/src/app/celeryworker_start.sh
RUN chmod +x /usr/src/app/celerybeat_start.sh
RUN chmod +x /usr/src/app/celeryworker_start.sh

# set permissions for flower start
COPY ./docker/flower/ .
RUN sed -i 's/\r$//g' /usr/src/app/flower_start.sh
RUN chmod +x /usr/src/app/flower_start.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
