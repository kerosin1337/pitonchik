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
