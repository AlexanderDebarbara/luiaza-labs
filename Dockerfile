FROM python:3.11.2-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update \
    && apt-get install -y \
        build-essential \
        gettext \
        gcc \
        python-dev \
        vim \
        libpq-dev \
    && apt-get -y clean

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

EXPOSE 8000