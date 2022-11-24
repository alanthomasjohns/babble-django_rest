from django.urls import path, include

from .views import *

from django.conf.urls.static import static

from django.urls import re_path as url



urlpatterns = [

    path('follow/', FollowUserAPIView.as_view(), name="url_follow"),                               #  Kullanıcıyı takip etme   (anında takip)
    path("unfollow/<follower__email>",UnfollowerUserAPIView.as_view(),name="url_follower"), 
    
    # #Follow
    # path('friends-now/', GetUserFriendsView.as_view(), name='get-friends-of-logged-in-user'),
    # path('unfriend/<int:user_id>/', UnfriendUserView.as_view(), name='unfriend-another-user'),
    # path('requests/', GetReceivedFriendRequests.as_view(), name='get-pending-friend-requests-received'),
    # path('requests/pending/', GetSendFriendRequests.as_view(), name='get-pending-friend-requests-sent'),
    # path('requests/<int:user_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    # path('requests/accept/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept-new-friend'),
    # path('requests/reject/<int:pk>/', RejectFriendRequestView.as_view(), name='reject-new-friend')
    
] 