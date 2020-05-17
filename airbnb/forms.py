from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Home

class HomeForm(forms.ModelForm):
  image = forms.ImageField()

  class Meta:
    model = Home
    fields = ('image','name', 'description', 'price')    