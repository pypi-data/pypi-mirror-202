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
