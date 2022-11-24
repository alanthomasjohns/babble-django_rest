
from . models import Post
from rest_framework import serializers
from  comment.serializers import CommentSerializer
from votes.serializers import VoteSerializer
class PostSerializer(serializers.ModelSerializer):
    posted_user = serializers.ReadOnlyField(source='owner.email')
    # myparent = serializers.SerializerMethodField(read_only=True)
    comments=CommentSerializer(many=True,read_only=True)
    votes=VoteSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ['id','posted_user', 'caption','post_image','post_video','location','post_date','posted_time','saves','votes','comments']


    def get_myparent(self,obj):
        serializer = PostSerializer(obj.parent,
        context={'request':self.context.get('request')})
        return serializer.data

        