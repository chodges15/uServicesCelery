import os
from celery import Celery
import pprint

app = Celery('message_location')


@app.task
def fetch_message_location(message):
    pprint(message)
