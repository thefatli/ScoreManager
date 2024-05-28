from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'identified_check']
        ref_name = "CustomUserCreateSerializer"  

class UserCreateSerializer2(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password']
        ref_name = "CustomUserCreateSerializer2"  

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email']
        ref_name = "CustomUserSerializer"  

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'image']
