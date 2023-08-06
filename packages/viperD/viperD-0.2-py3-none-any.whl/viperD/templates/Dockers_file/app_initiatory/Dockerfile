FROM ubuntu_image

# RUN bash


# FROM python:3.8.2
# set the docker working dir to /__viper__
WORKDIR /__viper__

ENV DEBIAN_FRONTEND=noninteractive

COPY ./requirements/requirements.txt .
COPY ./requirements/requirements.py .

RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3.7 \
    python3-pip

RUN pip3 install -r requirements.txt
