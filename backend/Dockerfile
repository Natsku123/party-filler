# Development dockerfile

FROM natsku/uvicorn-gunicorn:python3.8-alpine3.12

RUN apk --update add build-base bash nano gcc musl-dev python3-dev libffi-dev openssl-dev mysql-client curl cargo && rm -rf /var/cache/apk/*

COPY . /app

WORKDIR /app

RUN chmod +x /app/prestart.sh

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install -r requirements.txt
