# syntax=docker/dockerfile:1

FROM python:3.11.0a2

WORKDIR /usr/app

COPY ./python /usr/app

COPY requirements.txt /usr/app

RUN pip install -r requirements.txt