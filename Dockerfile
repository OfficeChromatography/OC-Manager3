FROM python:buster
MAINTAINER Lucas M. Sing

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y v4l-utils
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
# Copy the app folder from system to docker
COPY ./app /app

# -D is only to run the apps without root premision
# RUN adduser user
# RUN adduser -D user
# USER user
