FROM __viper___app_backup

RUN bash

ENV DEBIAN_FRONTEND=noninteractive

RUN echo "conda activate __viper__" >> /root/.bashrc

WORKDIR /__viper__

COPY ./requirements/requirements.txt .
COPY ./requirements/requirements.py .

RUN pip3 install -r requirements.txt
RUN python3 requirements.py

