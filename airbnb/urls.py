from django.urls import path
from . import views

urlpatterns = [
    path('', views.accomodation_list, name='accomodation_list'),
]