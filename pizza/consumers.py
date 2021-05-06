import json
import random
from time import sleep

from channels.generic.websocket import WebsocketConsumer
from django.db.models import signals
from django.dispatch import receiver

from .models import *


# @receiver(signals.post_save, sender=Cart)
class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        cart = Order.objects.all()

        result = [{

            'phone': i.phone,
            'cart': i.cart,
            'address': i.address,
            'entrance': i.entrance,
            'floor_number': i.floor_number,
            'apartment_number': i.apartment_number,
            'status': i.status
        } for i in cart]
        self.send()
        sleep(1)
