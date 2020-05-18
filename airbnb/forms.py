from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Home

class HomeForm(forms.ModelForm):

  class Meta:
    model = Home
    fields = ('image','name', 'description', 'price')    