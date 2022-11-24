from django.db import models
from user.models import Account
from comment.models import Comment
from replies.models import Reply
from posts.models import Post
# Create your models here.
class Notification(models.Model):
  
    types = [
        ('L','love'),
        ('F','follow'),
        ('M','message'),
        ('R','reply'),
        ('P','post'),
        ('C','comment')
    ]
    notification_type = models.CharField(max_length=2,choices=types,default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='+', blank=True, null=True)

    to_user = models.ForeignKey(Account, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(Account, related_name='notification_from', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user_has_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'from {self.from_user} to {self.to_user}'