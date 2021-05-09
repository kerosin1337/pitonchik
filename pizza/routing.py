from django.urls import re_path
from .consumers import OrderWS

ws_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', OrderWS.as_asgi())
]
