from django.urls import path
from .consumers import OrderWS

ws_urlpatterns = [
        path('order/', OrderWS.as_asgi())
]
