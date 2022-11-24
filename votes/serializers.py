from .models import Vote, Reaction, Reacty
from rest_framework import serializers

class VoteCreateSerializer(serializers.ModelSerializer):
    # voted_by = serializers.ReadOnlyField(source='vote_type.email')
    class Meta:
        model   = Reaction
        fields  = ['id', 'post', 'vote_type']


class VoteSerializer(serializers.ModelSerializer):
    down_vote_by=serializers.ReadOnlyField(source='down_vote_by.email')
    up_vote_by = serializers.ReadOnlyField(source='up_vote_by.email')
    post_name = serializers.ReadOnlyField(source='post.content')
    class Meta:
        model = Vote
        fields = ['id','post', 'post_name','up_vote_by','down_vote_by']


class ReactySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reacty
        fields = '__all__'



# class VoteSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model   = Vote
#         fields  = '__all__'
    
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['voter_name']= f'{instance.voter.first_name} {instance.voter.last_name}'
    #     return response