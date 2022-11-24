
from rest_framework import mixins, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, DestroyAPIView, get_object_or_404, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import generics,filters
from friends import my_mailer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .serializers import *
from .models import FollowAPI
from rest_framework.permissions import IsAuthenticated,AllowAny
from user.models import Account
from helpers.my_mailer import *
from user.serializers import *
from rest_framework.exceptions import PermissionDenied, NotFound
from .serializers import FollowSerializer
from .models import *
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
import random
from user.serializers import UserSerializer


class FollowUnfollowUserView(CreateAPIView, mixins.DestroyModelMixin):
    """
    post: follow user with <user_id>
    delete: unfollow user with user_id
    """
    # lookup_field = 'user_id'  # not needed here but can be useful to replace 'pk' with something else
    serializer_class = FollowSerializer
    queryset = FollowAPI.objects.all()

    def perform_create(self, serializer):
        user_to_follow = get_object_or_404(Account, id=self.kwargs.get('user_id'))
        already_following = FollowAPI.objects.filter(follower=self.request.user, followee=user_to_follow).exists()

        if already_following:
            raise PermissionDenied('already following')

        my_mailer.new_follower(user_to_follow, self.request.user)
        serializer.save(follower=self.request.user, followee=user_to_follow)

    def delete(self, request, *args, **kwargs):
        user_to_unfollow = get_object_or_404(Account, id=self.kwargs.get('pk'))
        follow = get_object_or_404(FollowAPI, follower=self.request.user, followee=user_to_unfollow)
        follow.delete()
        return Response(status=204)



class CreateFollowAPIView(generics.ListCreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = FollowAPI.objects.all()
    serializer_class = CustomFollowSerializer

class suggested_friends(generics.ListAPIView):
    authentication_classes=[TokenAuthentication,]
    # permission_classes=[is]
    def get(self, request, *args, **kwargs):
        
        friends=set()
        following_obj=FollowAPI.objects.filter(follower=request.user)
        items = list(following_obj)
        following_obj_set=set(following_obj)
        someFollowingObjs = random.sample(items, int(len(items)))
        
        
        for i in range(len(someFollowingObjs)):
            following_id=someFollowingObjs[i].following
            following_following_obj=FollowAPI.objects.filter(follower=following_id)
            items = list(following_following_obj)
            somefollowing_following_Objs = random.sample(items, int(len(items)))
            seti=set()
            
            for j in range(len(somefollowing_following_Objs)):
                if(somefollowing_following_Objs[j].following==request.user):
                    continue
                seti.add(somefollowing_following_Objs[j])

            for i in seti:
                friends.add(i)
        friends.difference(following_obj_set)
        j=0
        data={'suggested_friends':[]}
        for i in friends:
            data['suggested_friends'].append(UserSerializer( i.following).data)
            j+=1
            if j>10:
                break
            
        return Response(data,status=202)

class UnfollowerUserAPIView(DestroyAPIView):
    #Takipten çık
    lookup_field     = "follower__email"
    serializer_class = FollowSerializer
    queryset         = FollowAPI.objects.all()

    def get_object(self):
        follower = get_object_or_404(Account,username=self.kwargs.get("follower__email"))
        following=self.request.user
        return get_object_or_404(Account,follower=follower,following=following)

    # def perform_destroy(self, instance):
    #     ModelNotification.objects.filter(receiver_user=instance.follower,sender_user=self.request.user,post=None).delete()
    #     instance.delete()

class FollowUserAPIView(CreateAPIView):
    # Herkese açık hesabı takip et
    serializer_class  = FollowSerializer
    queryset          = Account.objects.all()

    def perform_create(self, serializer):
        # Takip ederken karşı tarafa bildirim de gönderiyoruz
        receiver_user = get_object_or_404(Account,email=serializer.validated_data["follower"].get("email"))
        sender_user   = self.request.user
        # ModelNotification.objects.create(receiver_user=receiver_user,sender_user=sender_user,notificationType=2)
        serializer.save(follower=receiver_user,following=sender_user)
        