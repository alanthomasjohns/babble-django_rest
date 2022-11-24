from rest_framework import serializers
from . models import Comment
from replies.serializers import ReplySerializer
class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source='owner.email')
    replys=ReplySerializer(many=True,read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'commented','comment_image','comment_date','commented_by','comment_time','replys','post']