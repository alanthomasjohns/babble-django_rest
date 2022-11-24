from django.db import models
from django.db.models.signals import post_save, post_delete
from user.models import Account
from notifications.models import Notification


class FriendStatus:
    pending = 'PENDING'
    accepted = 'ACCEPTED'
    declined = 'DECLINED'


FRIEND_CHOICES = (
    (FriendStatus.pending, 'PENDING'),
    (FriendStatus.accepted, 'ACCEPTED'),
    (FriendStatus.declined, 'DECLINED'),
)


class FollowAPI(models.Model):
    follower = models.ForeignKey(Account,on_delete=models.CASCADE, null=True, related_name='follower')
    following = models.ForeignKey(Account,on_delete=models.CASCADE, null=True, related_name='following')
    
    # class Meta:
    #     unique_together = ['follower', 'following']

    def __str__(self):
        return str(str(self.follower) + ' follows ' + str(self.following))
    

    # def user_follow(sender, instance, *args, **kwargs):
    #     follow = instance
    #     sender = follow.follower
    #     following = follow.following
    #     notify = Notification(sender=sender, user=following, notification_type=3)
    #     notify.save()

    # def user_unfollow(sender, instance, *args, **kwargs):
    #     follow = instance
    #     sender = follow.follower
    #     following = follow.following

    #     notify = Notification.objects.filter(sender=sender, user=following, notification_type=3)
    #     notify.delete()

    

# post_save.connect(FollowAPI.user_follow, sender=FollowAPI)
# post_delete.connect(FollowAPI.user_unfollow, sender=FollowAPI)

# class Follow(models.Model):
#     follower = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='follower', null=True, blank=True)
#     followee = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='followee',  null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True, blank=True)

#     def __str__(self):
#         return f'{self.follower} follows {self.followee}'


# class Friend(models.Model):
#     sender = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
#     receiver = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='receiver',  null=True, blank=True)
#     status = models.CharField(max_length=9, choices=FRIEND_CHOICES, default=FriendStatus.pending)
#     created = models.DateTimeField(auto_now_add=True, blank=True)

#     def __str__(self):
#         return f'friend request from {self.sender} to {self.receiver}'