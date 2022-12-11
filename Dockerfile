FROM python:3.9

RUN \
  apt-get update \
  && apt-get -y install gettext-base \
  && apt-get -y install gettext \
  && apt-get -y install default-mysql-client \
  && apt-get -y install lsb-release \
  && apt-get -y install netcat \
  && apt-get -y install libicu-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONUTF8=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
