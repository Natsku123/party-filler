# Development dockerfile

#FROM natsku/uvicorn-gunicorn:python3.8-alpine3.12
FROM tiangolo/uvicorn-gunicorn:python3.8-slim

ARG BUILD_VERSION


RUN apt-get update && apt-get install -y mariadb-client

#RUN apk --update add build-base bash nano gcc musl-dev python3-dev libffi-dev openssl-dev mysql-client curl cargo && rm -rf /var/cache/apk/*

COPY . /app

WORKDIR /app

RUN chmod +x /app/prestart.sh

RUN date +%Y.%m.%d > .build

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV VERSION=${BUILD_VERSION}

RUN pip install -r requirements.txt
