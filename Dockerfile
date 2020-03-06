FROM python:3.7-slim
WORKDIR /workdir
RUN apt-get -y update
ENV LANG en_US.utf8
COPY requirements.txt /workdir
COPY requirements-dev.txt /workdir
RUN pip install -r requirements.txt -r requirements-dev.txt
