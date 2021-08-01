# pull official base image
FROM ubuntu:focal

RUN mkdir -p /home/django
ENV DJANGO_HOME=/home/django
WORKDIR $DJANGO_HOME

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy and install requirements
COPY ./requirements ./requirements

RUN chmod +x requirements/ubuntu-requirements.sh
RUN requirements/ubuntu-requirements.sh

#RUN groupadd -r django && useradd -r -g django django
RUN adduser --disabled-password --gecos '' django
RUN chown -R django:django $DJANGO_HOME
RUN mkdir /appenv
RUN chown -R django:django /appenv

USER django

ENV VIRTUAL_ENV=/appenv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade setuptools wheel
RUN pip install -r requirements/requirements.txt

# Copy app
COPY . .

USER root
RUN mkdir -p $DJANGO_HOME/static
RUN mkdir -p $DJANGO_HOME/media

# Collect static files
RUN python manage.py collectstatic --noinput --clear
RUN chmod 755 -R $DJANGO_HOME/static
RUN chmod 755 -R $DJANGO_HOME/media
RUN chown -R django:django $DJANGO_HOME
RUN chmod +x entrypoint.sh

USER django
# run entrypoint.sh
ENTRYPOINT ["/home/django/entrypoint.sh"]