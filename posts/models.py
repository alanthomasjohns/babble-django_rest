""" IG Post Model """
from django.db import models
from django.conf import settings
from user.models import Account



class Post(models.Model):
    owner = models.ForeignKey(Account, related_name='posts', on_delete=models.CASCADE)
    caption=models.CharField(max_length=40)
    post_image=models.ImageField(upload_to="post_image",null=True,blank=True)
    post_video=models.ImageField(upload_to="post_video",null=True,blank=True)
    post_date=models.DateField(auto_now_add=True, null=True)
    posted_time = models.DateTimeField('Post_posted_time', auto_now_add=True)
    votess = models.ManyToManyField(Account, related_name='votess')
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name='parentpost', null=True, blank=True)
    saves = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="Post_Saves",
                                   blank=True,
                                   symmetrical=False)
    location = models.CharField('Location', max_length=30, blank=True)
    def __str__(self):
        return self.caption

    @property
    def is_parent(self):
        return True if self.parent is None else False





