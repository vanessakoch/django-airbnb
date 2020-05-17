from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_list, name='home_list'),
    path('home/<int:pk>/', views.home_detail, name='home_detail'),
    path('home/new/', views.home_new, name='home_new'),
    path('home/<int:pk>/edit/', views.home_edit, name='home_edit'),
]