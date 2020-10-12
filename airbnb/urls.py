from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('', views.init_page, name='init_page'),
    path('home/', views.home_list, name='home_list'),
    path('home/search/', views.search_list, name='search_list'),    
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

    # Rest
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('rest/home/', views.rest_home_list, name='rest_home_list'),
    path('rest/home/<pk>/', views.rest_home_detail, name='rest_home_detail'),
    path('rest/user/', views.rest_user_list, name='rest_user_list'),
    path('rest/user/<pk>/', views.rest_user_detail, name='rest_user_detail'),
    path('rest/post/', views.rest_post_list, name='rest_post_list'),
    path('rest/post/<pk>/', views.rest_post_detail, name='rest_post_detail')


    
]