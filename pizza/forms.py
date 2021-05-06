from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import *


class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']


# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment']
