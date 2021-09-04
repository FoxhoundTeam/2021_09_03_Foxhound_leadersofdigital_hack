ARG PYTHON_VERSION=3.8.10-slim-buster

FROM python:${PYTHON_VERSION} as python

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  python3-dev \
  pkg-config

COPY ./dependencies.sh .
COPY ./backend/requirements.txt .
RUN chmod +x /dependencies.sh

# Create Python Dependency
RUN ./dependencies.sh
RUN pip3 install -r requirements.txt

COPY ./rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/

RUN apt-get remove -y build-essential \
  python3-dev \
  pkg-config && apt-get autoremove -y && apt-get purge -y


ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/webapp

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

COPY ./compose/web/docker-entrypoint.sh /docker-entrypoint.sh
RUN sed -i 's/\r$//g' /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh


COPY ./compose/web/commands/ /commands
RUN sed -i 's/\r$//g' /commands/*
RUN chmod +x -R /commands


COPY ./compose/web/uwsgi.ini /webapp/uwsgi.ini

ENV UWSGI_WORKERS 4
ENV UWSGI_THREADS 1

# copy application code to WORKDIR
COPY ./backend ${APP_HOME}

ENTRYPOINT ["/docker-entrypoint.sh"]