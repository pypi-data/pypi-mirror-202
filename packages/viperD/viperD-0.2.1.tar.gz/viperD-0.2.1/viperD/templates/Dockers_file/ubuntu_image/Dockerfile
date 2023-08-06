# Base Image

#################################################
#### __________System dependencies___________  ####

# system dependencies
FROM ubuntu:20.04 AS system

# install timezone package
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && rm -rf /var/lib/apt/lists/*

# system dependencies
RUN apt-get update && apt-get install -y build-essential zlib1g-dev libffi-dev libpq-dev software-properties-common ca-certificates

# leverage the ca-certificates ubuntu package to ensure fresh ca certs are in the image
RUN update-ca-certificates --fresh

# utilities and tools. install and setup.
FROM system AS utilities

# useful unix tooling
RUN apt-get update && apt-get install -y git curl rsync lsof jq unzip tree wait-for-it zip

# aws cli for interacting with web services
RUN apt-get update && apt-get install -y awscli

RUN apt-get install -y libxml2-dev libxslt-dev python-dev


###################################################
#### __________Minconda setup___________  ####

# install anaconda for python development
# FROM utilities AS conda-install

# install miniconda to /miniconda
# RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# conda install script and cleanup
# RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b && rm Miniconda3-latest-Linux-x86_64.sh

# set conda executable
# ENV PATH=/miniconda/bin:${PATH}

# update to the latest version of conda if there has been a patch release
# RUN conda update -y conda

# update conda to the latest version if it is not already
# RUN conda update -n base -c defaults conda

# install anaconda for python development
# FROM conda-install AS environment-setup

#################################################


# initialize the prefered conda shell. This modifies bashrc to ensure shell context is correct
# RUN conda init bash

# create the conda environment
# all python related commands, tests, and long running processes
# should be executed in this conda environment

# do not auto activate the base environment
# RUN conda config --set auto_activate_base false