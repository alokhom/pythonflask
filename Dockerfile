# syntax=docker/dockerfile:1

FROM --platform=linux/arm64 python:3.8-slim-buster as build

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y git
RUN pip3 install -r requirements.txt

COPY . .
# Add this:
ENV FLASK_APP=flaskapp.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]