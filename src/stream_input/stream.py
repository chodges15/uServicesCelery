from celery import Celery
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pprint import pprint
import os

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass

    def presence(self, pubnub, presence):
        pprint(presence.__dict__)

    def message(self, pubnub, message):
        pprint(message.__dict__)


app = Celery("stream")

pnconfig = PNConfiguration()
pnconfig.ssl = False
pnconfig.subscribe_key = os.environ.get("PUBNUB_SUBSCRIBE_KEY")

pubnub = PubNub(pnconfig)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("keep-alive").execute()

print("Waiting for task to start subscribe...")


@app.task
def start(channel_name, key):
   pubnub.subscribe().channels(channel_name).execute()

@app.task
def stop(channel_name):
    pubnub.unsubscribe().channels(channel_name)

