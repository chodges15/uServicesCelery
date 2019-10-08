from celery import Celery
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import os

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass

    def presence(self, pubnub, presence):
        pass

    def message(self, pubnub, message):
        app.send_task('message_location.fetch_message_location', kwargs={'message': message}).delay()


app = Celery("stream")
app.conf.task_routes = {
    'http.*': {'queue': 'http_queue'},
    'stream.*': {'queue': 'stream_queue'},
    'message_location.*': {'queue': 'message_location_queue'},
}

pnconfig = PNConfiguration()
pnconfig.ssl = False
pnconfig.subscribe_key = os.environ.get("PUBNUB_SUBSCRIBE_KEY")

pubnub = PubNub(pnconfig)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("keep-alive").execute()


@app.task(queue="stream_input")
def start(channel_name):
   pubnub.subscribe().channels(channel_name).execute()


@app.task(queue="stream_input")
def stop(channel_name):
    pubnub.unsubscribe().channels(channel_name)

