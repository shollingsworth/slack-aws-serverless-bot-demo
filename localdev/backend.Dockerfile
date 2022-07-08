FROM python:3.9-slim-bullseye

ARG UID

RUN test "${UID}" || { echo "Failed to run with UID ${UID}"; exit 1; }
RUN apt update && apt install -y python3-pip curl
RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN useradd -m -s /bin/bash -u "${UID}" user
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list
RUN apt update && apt install -y yarn npm
USER user
