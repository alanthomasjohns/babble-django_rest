from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets,status,permissions,serializers
from django.shortcuts import get_object_or_404, render
from posts.models import Post
from rest_framework import views, generics
from .permissions import hasSelfVotedOrReadOnly
from .models import Vote, Reaction, Reacty
from .serializers import VoteSerializer, VoteCreateSerializer, ReactySerializer
from rest_framework.response import Response



class VoteViewSet(viewsets.ModelViewSet):
    queryset=Vote.objects.all()
    serializer_class=VoteSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly,hasSelfVotedOrReadOnly]
    
    def perform_create(self, serializer):
        post_instance=get_object_or_404(Post,pk=self.request.data['post'])

        #if user likes the post
        if self.request.data['up_vote']:
            already_up_voted=Vote.objects.filter(post=post_instance,up_vote_by=self.request.user).exists()
            print(already_up_voted)
            if already_up_voted:
                raise serializers.ValidationError({"message":"You have already liked this post"})
            else:
                serializer.save(up_vote_by=self.request.user,post=post_instance)
            # Notification.objects.create(notification_type='vote', from_user=receiver, to_user=sender)
        #if dislikes
        else:
            already_down_voted=Vote.objects.filter(post=post_instance,down_vote_by=self.request.user).exists()
            if already_down_voted:
                raise serializers.ValidationError({"message":"You have already disliked this post"})
            else:
                serializer.save(down_vote_by=self.request.user,post=post_instance)




class ReactPost(viewsets.ModelViewSet):
    queryset=Reaction.objects.all()
    serializer_class=VoteCreateSerializer
    # permission_classes=[permissions.IsAuthenticatedOrReadOnly,hasSelfVotedOrReadOnly]

    def perform_create(self, serializer):
        pass
        # post_instance=get_object_or_404(Reaction,pk=self.request.data['post'])
        # print(post_instance,"**************************************")

        # #if user likes the post
        # if self.request.data['celebrate']:
        #     print("*******************pp*******************")
        #     already_celebrated=Reaction.objects.filter(post=post_instance,voter=self.request.user).exists()
        #     print(already_celebrated, "********************************************")
        #     if already_celebrated:
        #         raise serializers.ValidationError({"message":"You have already liked this post"})
        #     else:
        #         serializer.save(voter=self.request.user,post=post_instance)
        #     # Notification.objects.create(notification_type='vote', from_user=receiver, to_user=sender)
        # #if dislikes
        # else:
        #     print("lsdjvksiubcziiwbidwibfkjdc")




class ReactyViewSet(viewsets.ModelViewSet):
    queryset = Reacty.objects.all()
    serializer_class = ReactySerializer

    def perform_create(self, serializer):
        post_instance=get_object_or_404(Post,pk=self.request.data['post'])


        if self.request.data['like1']:
            already_liked=Reacty.objects.filter(post=post_instance,like=self.request.user).exists()
            print(already_liked)
            if already_liked:
                raise serializers.ValidationError({"message":"You have already liked this post"})
            else:
                serializer.save(like=self.request.user,post=post_instance)
            # Notification.objects.create(notification_type='vote', from_user=receiver, to_user=sender)
        #if dislikes
        elif self.request.data['celebrate1']:
            already_celebrated=Reacty.objects.filter(post=post_instance,celebrate=self.request.user).exists()
            print(already_celebrated)
            if already_celebrated:
                raise serializers.ValidationError({"message":"You have already celebrated this post"})
            else:
                serializer.save(celebrate=self.request.user,post=post_instance)

        elif self.request.data['support1']:
            already_supported=Reacty.objects.filter(post=post_instance,support=self.request.user).exists()
            print(already_supported)
            if already_supported:
                raise serializers.ValidationError({"message":"You have already supported this post"})
            else:
                serializer.save(celebrate=self.request.user,post=post_instance)

        elif self.request.data['love1']:
            already_loved=Reacty.objects.filter(post=post_instance,love=self.request.user).exists()
            print(already_loved)
            if already_loved:
                raise serializers.ValidationError({"message":"You have already loved this post"})
            else:
                serializer.save(love=self.request.user,post=post_instance)

        elif self.request.data['insightful1']:
            already_insighted=Reacty.objects.filter(post=post_instance,insightful=self.request.user).exists()
            print(already_insighted)
            if already_insighted:
                raise serializers.ValidationError({"message":"You have already insighted this post"})
            else:
                serializer.save(insightful=self.request.user,post=post_instance)

        elif self.request.data['curious1']:
            already_curious=Reacty.objects.filter(post=post_instance,curious=self.request.user).exists()
            print(already_curious)
            if already_curious:
                raise serializers.ValidationError({"message":"You have already celebrated this post"})
            else:
                serializer.save(curious=self.request.user,post=post_instance)

        else :
            pass

        


    



class VoteGetView(views.APIView):
    
    def get_post(self, post_id):
        try:
            return Post.objects.get(id = post_id)
        except:
            raise Http404    
    
    def get(self, request, post_id):
        post = self.get_post(post_id)
        vote_list = dict()
        vote_list.update({'like': post.votes.filter(vote_type = 'like').count()})
        vote_list.update({'celebrate': post.votes.filter(vote_type = 'celebrate').count()})
        vote_list.update({'support': post.votes.filter(vote_type = 'support').count()})
        vote_list.update({'love': post.votes.filter(vote_type = 'love').count()})
        vote_list.update({'insightful': post.votes.filter(vote_type = 'insightful').count()})
        vote_list.update({'curious': post.votes.filter(vote_type = 'curious').count()})        
        return Response(vote_list, status=status.HTTP_200_OK)

        
    
    
class VotePostView(views.APIView):
    def post(self, request, post_id, vote_type):
        post = get_object_or_404(Post, id = post_id)
        choice  = request.data.get('vote_type')
        print(choice, "***************************************")
        user    = request.user 
        print(user, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        votes   = post.votess.all()
        print(votes, "**********************************************")
        
        for vote in votes:
            if user == vote.voter:
                if int(choice) > 0:
                    return Response({'detail': "Already voted"}, status=status.HTTP_226_IM_USED)
                post.votess.filter(voter = user).delete()
                try:
                    pass
                    # Notification.objects.get(target = post.written_by, source = user,
                    #                          action = 'post_liked', action_id = post_id).delete()
                except:
                    pass
                return Response({'detail': "Vote Removed"}, status = status.HTTP_202_ACCEPTED)
        
        if int(choice) > 0:
            data = dict()
            data.update({'post':post_id, 'vote_type': vote_type, 'voter':user.id})
            serializer = VoteCreateSerializer(data = data, context = {'request': request})
            if serializer.is_valid():
                serializer.save()
                target = post.owner
                if target != user:
                    pass
                    # Notification.objects.create(target = target, source = user, action = 'post_liked', 
                    #                             detail = 'liked your post.', action_id = post_id)
                return Response({'detail':'Voted'},status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Post must be upvoted first.'},status=status.HTTP_400_BAD_REQUEST)