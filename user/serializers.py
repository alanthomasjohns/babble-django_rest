from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','username','first_name', 'last_name','email', 'password', 'account_type','is_verified']



class UserLessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username','email','account_type']
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = UserProfile
        fields  = '__all__'


class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'birthday', 'gender', 'profile_pic', 'account_type', 'phone_number']


class UserProfileSearchSerailizer(serializers.Serializer):
    profile_id = serializers.CharField(source = 'id')
    
    class Meta:
        model = UserProfile
        fields = ('profile_id')
        
    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['name'] = f'{instance.first_name} {instance.last_name}'
        response['avatar'] = self.get_avatar(instance)
        response['tagline'] = instance.social_profile.tagline
        return response    
    
    def get_avatar(self, instance):
        try:
            name = instance.avatar.url
            url = self.context['request'].build_absolute_uri(name)
            return url
        except:
            return None


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name']


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()