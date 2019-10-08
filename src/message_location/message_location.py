import os
from celery import Celery
import json

app = Celery('message_location')
app.conf.task_routes = {
    'http_interface.*': {'queue': 'http_queue'},
    'stream_input.*': {'queue': 'stream_queue'},
    'message_location.*': {'queue': 'message_location_queue'},
}


@app.task
def fetch_message_location(message):
    print(message["place"]["full_name"])
    app.send_task('http_interface.show_user_event_location', kwargs={'location': message["place"]["full_name"]})
