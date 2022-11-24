

from django.urls import path
from .views import *

app_name = 'feed'

urlpatterns = [
    path('followees/', ListUserFollowingPostsView.as_view(), name='list-posts-of-followed-users'),
    path("post/retweet/<int:id>/", RePostView.as_view() , name="repost-view"),
]