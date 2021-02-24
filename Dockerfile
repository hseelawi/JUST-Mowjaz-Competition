FROM ubuntu:20.04

RUN apt-get clean &&  \
    apt-get update && \
    apt-get install -yq --no-install-recommends python3.8-dev \
						python3-pip \
						build-essential \
                                                locales \
                                                curl \
                                                unzip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade setuptools pip

## Locale information
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8   \
    LANGUAGE=en_US.UTF-8   \
    LC_ALL=en_US.UTF-8

## Create User and switch to user space
ENV APP_USER="just" \
    APP_DIR="/app"
RUN adduser --disabled-password --gecos "" "$APP_USER"

WORKDIR "$APP_DIR"
ADD . "$APP_DIR/"
# will be removed when we use the final model
ENV ARAVEC='https://bakrianoo.s3-us-west-2.amazonaws.com/aravec/full_uni_sg_300_twitter.zip'
RUN /bin/bash aravec.sh
RUN pip3 install --no-cache-dir --upgrade --requirement "$APP_DIR/requirements.txt"

## RUN APP
USER "$APP_USER"
EXPOSE 5000
CMD start_microservice
