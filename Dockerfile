# syntax=docker/dockerfile:1

FROM python:3.11.0a2-bullseye

WORKDIR /app

COPY ./* .

RUN pip install -r requirements.txt
