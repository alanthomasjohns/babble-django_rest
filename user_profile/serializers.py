from dataclasses import fields
from user.models import UserProfile
from rest_framework import serializers

class profileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField (source = 'owner.username')
    class Meta:
        model = UserProfile
        fields = '__all__'
        
        