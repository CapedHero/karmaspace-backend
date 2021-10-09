FROM python:3.8.12-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN curl -sL https://git.io/tusk | bash -s -- -b /usr/local/bin latest

RUN mkdir /karmaspace-backend
WORKDIR /karmaspace-backend

COPY requirements/locked/dev.txt requirements/locked/dev.txt
RUN pip install -r requirements/locked/dev.txt

COPY . .
