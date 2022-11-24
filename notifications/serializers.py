from rest_framework import serializers
from .models import Notification
from user.serializers import UserLessInfoSerializer
from posts.serializers import PostSerializer
from comment.serializers import CommentSerializer

class NotificationSerializer(serializers.ModelSerializer):
    from_user = UserLessInfoSerializer(read_only=True)
    to_user = serializers.StringRelatedField(read_only=True)
    noti_count = serializers.SerializerMethodField(read_only=True)
    tweet = PostSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'
    
    def get_noti_count(self,obj):
        count = self.context.get('noti_count')
        return count