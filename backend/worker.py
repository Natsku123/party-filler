import os
import json
import requests
from celery import Celery
from pydantic import BaseModel
from typing import Union

app = Celery(__name__)
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@app.task
def send_webhook(url: str, data: Union[dict, str, BaseModel]):
    """ """
    if isinstance(data, dict):
        content = json.dumps(data)
    elif isinstance(data, str):
        content = data
    elif isinstance(data, BaseModel):
        content = data.json()
    else:
        raise ValueError("Cannot parse data")

    return requests.post(url, data=content)
