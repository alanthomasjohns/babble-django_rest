from rest_framework.status import HTTP_201_CREATED
from friends.models import FollowAPI
from notifications.models import Notification
from .serializers import PostSerializer
from rest_framework.views import APIView
from .models import Post
import datetime
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from user_profile.permissions import IsOwnerOrReadOnly
from rest_framework import status, viewsets, exceptions
from rest_framework.response import Response
class PostViewSet(viewsets.ModelViewSet):
    """
    Posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)




class RePostView(APIView):
    def post(self, request, id):
        his_post = Post.objects.get(id=id)
        print(his_post, "*********************************************")
        shared_post = Post.objects.create(
            owner = request.user,
            caption = his_post.caption,
            post_image=his_post.post_image,
            post_video=his_post.post_video,
            posted_time = datetime.datetime.now()
        )
        shared_post.save()

        sm = shared_post.id
        queryset = Post.objects.get(id=sm)
        serializer = PostSerializer(queryset)
        permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly]

        # # def perform_create(self, serializer):
        # #     serializer.save(owner=self.request.user)

        
            
        return Response(serializer.data)

# class RePostView(APIView):
#     def post(self, request):
#         data = request.data
#         post = Post.objects.all()
#         print("*******************************")
#         print(post)
#         print("*******************************")
#         post_id = data.get('id')
#         print(post_id)
#         # tweet = get_object_or_404(Tweet,id=tweetId)
#         try:
#             post = Post.objects.all()
#         except:
#             raise exceptions.APIException("Not Found ! ")
#         # if post.owner == request.user:
#         #     raise exceptions.APIException("Can't Retweet your own post")
#         # try:
#         parent_tweet = post.objects.filter(parent=post, author=request.user)
#         if parent_tweet.exists():
#             raise exceptions.APIException("Already retweeted !")
#         else:
#             re_tweet = post.objects.create(
#                 author=request.user,
#                 parent=post
#             )
#             Notification.objects.get_or_create(
#                     notification_type='RT',
#                     tweet=post,
#                     to_user=post.author,
#                     from_user=request.user)
#             serializer =  PostSerializer(re_tweet,context={"request":request})
#             return Response(serializer.data,status=HTTP_201_CREATED)



class ListUserFollowingPostsView(ListAPIView):
    """
    get: list all posts of followed users
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        following = FollowAPI.objects.filter(follower=self.request.user)
        followed_user_ids = [follow.following.id for follow in following]
        posts = Post.objects.filter(user__in=followed_user_ids)
        return posts.order_by('-created')