from celery import Celery
from pubnub.callbacks import SubscribeCallback
from pubnub.models.consumer.pubsub import PNMessageResult
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import os

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass

    def presence(self, pubnub, presence):
        pass

    def message(self, pubnub, pn_message_result: PNMessageResult):
        app.send_task('message_location.fetch_message_location', kwargs={'message': pn_message_result.message})


app = Celery("stream")
app.conf.task_routes = {
    'http_interface.*': {'queue': 'http_queue'},
    'stream_input.*': {'queue': 'stream_queue'},
    'message_location.*': {'queue': 'message_location_queue'},
}


pnconfig = PNConfiguration()
pnconfig.ssl = False
pnconfig.subscribe_key = os.environ.get("PUBNUB_SUBSCRIBE_KEY")

pubnub = PubNub(pnconfig)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(os.environ.get("PUBNUB_CHANNEL")).execute()


