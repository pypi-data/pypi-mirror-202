FROM ubuntu_image
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

# you can write your commands here which you want to run on terminal
# for e.g. 
# RUN your_command