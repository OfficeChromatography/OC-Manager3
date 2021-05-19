FROM python:3.7
MAINTAINER Lucas M. Sing

ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

RUN apt-get update && apt-get upgrade -y

RUN apt-get install python3-opencv python3-scipy python3-numpy -y
RUN apt-get install -y v4l-utils
RUN apt-get install curl -y

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip

# Installing Rust for compiling cryptography in ARMv7
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
RUN apt install build-essential libssl-dev libffi-dev rustc -y

RUN pip install -r /requirements.txt
RUN mkdir /app
WORKDIR /app
# Copy the app folder from system to docker
COPY ./app /app

RUN export PYTHONPATH='/usr/lib/python3/dist-packages'
ENV PYTHONPATH='/usr/lib/python3/dist-packages'

# -D is only to run the apps without root premision
# RUN adduser user
# RUN adduser -D user
# USER user
