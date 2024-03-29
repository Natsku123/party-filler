import os
import json
import datetime
from abc import ABC

import requests
from celery import Celery, Task
from celery.schedules import crontab

from typing import Union
from sqlmodel import Session
from core.database.crud import party as crud_party
from core.database import schemas, engine

app = Celery(__name__)
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")


# class SqlAlchemyTask(Task, ABC):
#     """An abstract Celery Task that ensures that the connection the the
#     database is closed on task completion"""
#
#     abstract = True
#
#     def after_return(self, status, retval, task_id, args, kwargs, einfo):
#         db_session.remove()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Check party status and send webhooks
    sender.add_periodic_task(crontab(), check_party_timeout.s())


# @app.task(base=SqlAlchemyTask)
@app.task
def check_party_timeout():
    with Session(engine) as db_session:
        # Get parties that are not locked and have timed out
        parties = crud_party.get_multi(
            db_session,
            limit=crud_party.get_count(db_session),
            filters={"end_time__le": datetime.datetime.now(), "locked": False},
        )

        for party in parties:
            webhook_data = {"party": party, "event": {"name": "on_party_timed_out"}}
            webhook = schemas.PartyTimedoutWebhook.parse_obj(webhook_data)

            # Send timeout webhook
            send_webhook.delay("http://bot:9080/webhook", webhook.json())

            # Lock party
            crud_party.lock(db_session, db_obj=party)


@app.task
def send_webhook(url: str, data: Union[dict, str]):
    """ """
    if isinstance(data, dict):
        content = json.dumps(data)
    elif isinstance(data, str):
        content = data
    else:
        raise ValueError("Cannot parse data")

    res = requests.post(url, data=content)

    return {"status": res.status_code, "data": res.text}
