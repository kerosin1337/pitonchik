from channels.generic.websocket import WebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Order)
class WSConsumer(WebsocketConsumer):
    order = Order.objects.all()
    result = [{

        'phone': i.phone,
        'address': i.address,
        'entrance': i.entrance,
        'floor_number': i.floor_number,
        'apartment_number': i.apartment_number,
        'status': i.status
    } for i in order]

    def connect(self):
        print(self)
        self.accept()

