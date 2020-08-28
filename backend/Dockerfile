# Development dockerfile

FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

RUN apk --update add bash nano gcc musl-dev python3-dev libffi-dev openssl-dev && rm -rf /var/cache/apk/*

COPY . /app

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install -r requirements.txt