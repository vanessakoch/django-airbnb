from rest_framework import serializers
from users.models import CustomUser
from blog.models import Post
from .models import Home


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['pk', 'owner', 'image', 'name', 'description', 'price', 'address']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'email', 'birth_date', 'password']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'author', 'title', 'text', 'views']

