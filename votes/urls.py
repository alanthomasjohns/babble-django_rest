from django.urls import re_path as url

from django.urls import path, include, re_path

from rest_framework import routers

from .views import * 



urlpatterns = [
    path('vote/<int:post_id>/<str:vote_type>/', VotePostView.as_view()),
    path('vote/view/<int:post_id>/', VoteGetView.as_view()),
    
]
