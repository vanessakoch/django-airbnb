from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Home, Address, Reserve, Comment, Rating, Search
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class HomeForm(forms.ModelForm):

  class Meta:
    model = Home
    fields = ('image','name', 'description', 'price')    

class AddressForm(forms.ModelForm):
  
  class Meta:
    model = Address
    fields = ('country','zipcode', 'state', 'city', 'street', 'phone')

class RatingForm(forms.ModelForm):
    
  class Meta:
    model = Rating
    fields = ('home', 'user', 'stars')

class ReserveForm(forms.ModelForm):

  class Meta:
    model = Reserve
    fields = ('initial_date', 'final_date', 'number_peoples')

class CommentForm(forms.ModelForm):

  class Meta:
    model = Comment
    fields = ('author', 'text')
    
class SearchForm(forms.ModelForm):

  class Meta:
    model = Search
    fields = ('local', 'number_of_days', 'number_of_peoples')