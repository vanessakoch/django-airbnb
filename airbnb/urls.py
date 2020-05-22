from django.urls import path
from . import views

urlpatterns = [
    path('', views.init_page, name='init_page'),
    path('home/', views.home_list, name='home_list'),
    path('home/new/', views.home_new, name='home_new'),
    path('home/<int:pk>/', views.home_detail, name='home_detail'),
    path('home/<int:pk>/address/', views.home_address, name='home_address'),
    path('home/<int:pk>/reservation/', views.home_reservation, name='home_reservation'),
    path('home/<int:pk>/edit/', views.home_edit, name='home_edit'),
    path('home/<int:pk>/publish/', views.home_publish, name='home_publish'),
    path('home/<int:pk>/remove/', views.home_remove, name='home_remove'),
    path('home/<int:pk>/comment/', views.add_comment_to_home, name='add_comment_to_home'),
    path('home/<int:pk>/rating/', views.rating, name='rating'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]