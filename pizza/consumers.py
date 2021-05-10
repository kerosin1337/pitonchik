import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Order


class OrderWS(WebsocketConsumer):
    order = Order.objects.all()
    result = [{
        'customer': i.customer.user.username,
        'products': [{str(j): {
            'product': j.product.name,
            'final_price': int(j.final_price),
            'qty': j.qty
        }} for j in i.cart.products.all()],
        'final_price': int(i.cart.final_price),
        'phone': i.phone,
        'address': i.address,
        'entrance': i.entrance,
        'floor_number': i.floor_number,
        'apartment_number': i.apartment_number,
        'status': i.status
    } for i in order]

    def connect(self):
        print(1)
        self.room_name = self.scope['url_route']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': self.result
            }
        )
        self.accept()

    def disconnect(self, close_code):
        print(2)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print(3)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': self.result
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        print(4)
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': self.result
        }))

    # def connect(self):
    #     order = Order.objects.all()
    #     result = [{
    #         'customer': i.customer.user.username,
    #         'products': [{str(j): {
    #             'product': j.product.name,
    #             'final_price': int(j.final_price),
    #             'qty': j.qty
    #         }} for j in i.cart.products.all()],
    #         'final_price': int(i.cart.final_price),
    #         'phone': i.phone,
    #         'address': i.address,
    #         'entrance': i.entrance,
    #         'floor_number': i.floor_number,
    #         'apartment_number': i.apartment_number,
    #         'status': i.status
    #     } for i in order]
    #     self.accept()
    #     self.send(json.dumps(result))
