from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Home, Comment, Rating

class HomeForm(forms.ModelForm):

  class Meta:
    model = Home
    fields = ('image','name', 'description', 'price')    

class CommentForm(forms.ModelForm):

  class Meta:
      model = Comment
      fields = ('author', 'text')

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('id', 'home', 'user', 'stars')