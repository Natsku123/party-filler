import os
import json
import datetime
from abc import ABC

import requests
from celery import Celery, Task
from pydantic import BaseModel
from typing import Union

from sqlalchemy.orm import scoped_session

from core.database import SessionLocal
from core.database.crud import party as crud_party
from core.database import schemas

app = Celery(__name__)
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

db_session = scoped_session(SessionLocal)


class SqlAlchemyTask(Task, ABC):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""

    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Check party status and send webhooks
    sender.add_periodic_task(60.0, check_party_timeout.s())


@app.task(base=SqlAlchemyTask)
def check_party_timeout():

    # Get parties that are not locked and have timed out
    parties = crud_party.get_multi(
        db_session,
        limit=crud_party.count(),
        filters={"end_time__le": datetime.datetime.now(), "locked": False},
    )

    for party in parties:
        webhook_data = {"party": party, "event": {"name": "on_party_timed_out"}}
        webhook = schemas.PartyTimedoutWebhook(**webhook_data)

        # Send timeout webhook
        send_webhook.delay("http://bot:9080/webhook", webhook)

        # Lock party
        crud_party.lock(db_session, db_obj=party)


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
