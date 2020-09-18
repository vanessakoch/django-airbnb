from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CustomUserCreationForm(UserCreationForm):

  class Meta:
      model = CustomUser
      fields = ('username', 'email', 'birth_date', )

  helper = FormHelper()
  helper.form_method = 'POST'
  helper.add_input(Submit('submit', 'Cadastrar', css_class='btn-salvar'))
      
class CustomUserChangeForm(UserChangeForm):
  
  class Meta:
      model = CustomUser
      fields = ('username', 'email', 'birth_date', )