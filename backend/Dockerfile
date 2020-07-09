# Development dockerfile

FROM python:3.8-alpine

RUN apk --update add bash nano gcc musl-dev python3-dev libffi-dev openssl-dev && rm -rf /var/cache/apk/*

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]