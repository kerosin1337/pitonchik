import json

from channels.generic.websocket import WebsocketConsumer


class OrderWS(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        self.send(text_data=json.dumps({
            'message': message
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
