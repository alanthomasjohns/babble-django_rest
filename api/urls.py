from django.views.generic import base
from user.views import *
from replies.views import ReplyViewSet
# from friends.views import *
from votes.views import VoteViewSet, ReactPost, ReactyViewSet
from comment.views import CommentViewSet
from posts.views import PostViewSet
# from notifications.views import *
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()

urlpatterns=[
    # path('chat/<int:sender>/<int:receiver>/', message_view.as_view()),
    # path('messages/', message_list.as_view()),
    # path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/blacklist/',BlacklistTokenUpdateView.as_view(),name="blacklist")
]

router.register(r'reacts', ReactyViewSet)
router.register(r'posts',PostViewSet)
router.register(r'comments',CommentViewSet)
router.register(r'reply', ReplyViewSet)
router.register(r'vote', VoteViewSet)
router.register(r'react', ReactPost)
# router.register(r'follow', FollowViewSet, basename="follow")
# router.register(r'unfollow', UnFollowViewSet.as_view(), basename="unfollow")
# router.register(r'notifications', NotificationAPIView, basename="notifications")
urlpatterns=urlpatterns+router.urls