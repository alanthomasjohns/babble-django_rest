from django.db import models
from comment.models import Comment
from user.models import Account
# Create your models here.
class Reply(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,related_name='comment',on_delete=models.CASCADE)
    reply=models.CharField(max_length=4000)
    reply_date=models.DateField(auto_now_add=True)
    reply_time = models.DateTimeField('reply_posted_time', auto_now_add=True)
    def __str__(self):
        return self.reply