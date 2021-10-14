FROM python:3.7 as base
MAINTAINER Lucas M. Sing

ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

RUN pip install --upgrade pip

RUN apt-get update && apt-get upgrade -y

RUN apt-get install python3-opencv -y
RUN apt-get install -y v4l-utils

#Libraries for scipy
RUN apt-get install gfortran libopenblas-dev liblapack-dev -y
RUN apt-get install curl -y

RUN export PYTHONPATH='/usr/lib/python3/dist-packages'
ENV PYTHONPATH='/usr/lib/python3/dist-packages'

COPY requirements/base.txt /base_requirements.txt
RUN pip install -r /base_requirements.txt
#RUN pip install numpy==1.20.3
#RUN pip install djangorestframework==3.12.4

# -D is only to run the apps without root premision
# RUN adduser user
# RUN adduser -D user
# USER user
