FROM python:3.7-slim

COPY . /bot

WORKDIR /bot

RUN pip3.7 install -r requirements.txt

ENTRYPOINT ["python3.7"]
CMD ["main.py"]