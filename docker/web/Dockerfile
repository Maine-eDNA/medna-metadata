# pull official base image
FROM python:3.9.6-slim

# set work directory
WORKDIR /app


# set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# Copy and install requirements
COPY ./requirements ./requirements

# set permissions for entrypoint.sh
RUN sed -i 's/\r$//g' /app/requirements/docker-requirements.sh
RUN chmod +x /app/requirements/docker-requirements.sh
RUN requirements/docker-requirements.sh

RUN pip install -r requirements/requirements.txt

# copy project
COPY . .

# set permissions for entrypoint.sh
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]