# import json
# from time import sleep
#
# from channels.generic.websocket import WebsocketConsumer
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import *
#
#
# class WSConsumer(WebsocketConsumer):
#
#     def connect(self):
#         self.accept()
#         self.send('123')
#
#     def disconnect(self, code):
#         pass
#
#     def receive(self, text_data):
#         print(json.loads(text_data))
#
#     # def connect(self):
#     #     order = Order.objects.all()
#     #     result = [{
#     #         'customer': i.customer.user.username,
#     #         'products': [{str(j): {
#     #             'product': j.product.name,
#     #             'final_price': int(j.final_price),
#     #             'qty': j.qty
#     #         }} for j in i.cart.products.all()],
#     #         'final_price': int(i.cart.final_price),
#     #         'phone': i.phone,
#     #         'address': i.address,
#     #         'entrance': i.entrance,
#     #         'floor_number': i.floor_number,
#     #         'apartment_number': i.apartment_number,
#     #         'status': i.status
#     #     } for i in order]
#     #     self.accept()
#     #     self.send(json.dumps(result))
