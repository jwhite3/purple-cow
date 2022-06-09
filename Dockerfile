########
# BASE #
########

# pull official base image
FROM python:3.10-slim as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# apt uppgrade
RUN apt-get clean all && \
  apt-get update && \
  apt-get upgrade -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN addgroup --system cow \
    && adduser --system --ingroup cow cow


###########
# BUILDER #
###########

# pull from base image
FROM base as builder

# set noninterative mode
ENV DEBIAN_FRONTEND noninteractive

# apt install build requirements
RUN apt-get update && \
  apt-get install -y  \
      build-essential \
      libbz2-dev \
      libcurl4-openssl-dev &&\
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# create python virtual env and upgrade pip
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --upgrade pip

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements/requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r /requirements/requirements.txt

# TODO: Add documents builder

#########
# FINAL #
#########

# pull from base image
FROM base

# apt install runtime requirements
RUN apt-get update && \
  apt-get install -y  \
      libcurl4 && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# copy installed dependencies from builder
COPY --from=builder /opt/venv /opt/venv

# copy app code
COPY . /app

USER cow

ENV UVICORN_PORT ${UVICORN_PORT:-"3000"}

EXPOSE $UVICORN_PORT

# default command
CMD ["/opt/venv/bin/python", "-m", "uvicorn", "cow.app.main:app"]