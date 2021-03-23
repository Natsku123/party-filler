FROM python:3.9-alpine

RUN apk update && apk add python3-dev gcc libc-dev mysql-client build-base

COPY . /bot

WORKDIR /bot

RUN pip3.9 install -r requirements.txt

ENTRYPOINT ["python3.9"]
CMD ["main.py"]