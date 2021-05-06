import json
import random

from channels.generic.websocket import WebsocketConsumer
from time import sleep


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(json.dumps({'massage': random.randint(1, 100)}))
        sleep(1)
