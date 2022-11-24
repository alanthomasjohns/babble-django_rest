from rest_framework import serializers, exceptions

from .models import  FollowAPI
from user.serializers import UserSerializer, UserProfileSerializer


class FollowSerializer(serializers.ModelSerializer):

    """Serializer for listing all followers"""
    followed_user = serializers.CharField(source="follower.email")

    class Meta:
        model = FollowAPI
        fields = ("followed_user",)


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowAPI
        fields = ['id', 'sender', 'receiver', 'status']
        read_only_fields = ['id', 'sender', 'receiver']
        


class CustomFollowSerializer(serializers.ModelSerializer):
    # follower=serializers.CharField(source='follower.user_name')
    # following=serializers.CharField(source='following.user_name')
    class Meta:
        model = FollowAPI
        fields = '__all__'   