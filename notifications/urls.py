

from django.urls import path
from .views import *


urlpatterns = [
    path('notification_list/', NotificationView, name="notification-list"),
    path('notification_seen_delete/',
         NotificationSeen.as_view(), name="notification-seen"),
]