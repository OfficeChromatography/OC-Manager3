FROM python:rc-buster
MAINTAINER Lucas M. Sing

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
RUN mkdir /app
WORKDIR /app
# Copy the app folder from system to docker
COPY ./app /app

# -D is only to run the apps without root premision
# RUN adduser user
# RUN adduser -D user
# USER user
