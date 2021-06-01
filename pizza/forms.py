from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import UserData


class RegForm(UserCreationForm):
    class Meta:
        model = UserData
        fields = ('username', 'phone')


class UpdateUserData(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ('username', 'phone')
# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment']
