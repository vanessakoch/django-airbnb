from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Home, Address, Comment, Rating

class HomeForm(forms.ModelForm):

  class Meta:
    model = Home
    fields = ('image','name', 'description', 'price')    

class AddressForm(forms.ModelForm):
  
  class Meta:
    model = Address
    fields = ('country','zipcode', 'state', 'city', 'street', 'phone')   

class CommentForm(forms.ModelForm):

  class Meta:
      model = Comment
      fields = ('author', 'text')

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('home', 'user', 'stars')