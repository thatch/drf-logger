FROM python:3.7-slim
WORKDIR /workdir
RUN apt-get -y update
ENV LANG en_US.utf8
COPY . /workdir
RUN python setup.py develop
