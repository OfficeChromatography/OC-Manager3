FROM python:3.7-alpine
MAINTAINER Lucas M. Sing

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
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
