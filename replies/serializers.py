from rest_framework import serializers
from . models import Reply
class ReplySerializer(serializers.ModelSerializer):
    replied_by = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Reply
        fields = ['id', 'reply','reply_date','replied_by','reply_time','comment']