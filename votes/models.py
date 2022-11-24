from django.db import models
from posts.models import Post
from user.models import Account
# Create your models here.



class Reaction(models.Model):
   CHOICE = (  
             ('like','like'),
             ('celebrate','celebrate'),
             ('support','support'),
             ('love','love'),
             ('insightful','insightful'),
             ('curious','curious')
            )
   
   post              = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "votesm", null=True)
   vote_type         = models.CharField(choices = CHOICE, default = None, max_length = 10)
   voter             = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = "votesm", null=True)





class Reacty(models.Model):
   post              = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "react", null=True)
   like              = models.ForeignKey(Account, related_name='like_react',on_delete=models.CASCADE,default=None,blank=True,null=True)
   celebrate         = models.ForeignKey(Account, related_name='celebrate_react',on_delete=models.CASCADE,default=None,blank=True,null=True)
   support           = models.ForeignKey(Account, related_name='support_react',on_delete=models.CASCADE,default=None,blank=True,null=True)
   love              = models.ForeignKey(Account, related_name='love_react',on_delete=models.CASCADE,default=None,blank=True,null=True)
   insightful        = models.ForeignKey(Account, related_name='insightful_react',on_delete=models.CASCADE,default=None,blank=True,null=True)
   curious           = models.ForeignKey(Account, related_name='curious_react',on_delete=models.CASCADE,default=None,blank=True,null=True)





class Vote(models.Model):
    post=models.ForeignKey(Post,related_name='votes',on_delete=models.CASCADE)
    up_vote_by = models.ForeignKey(Account,related_name='up_vote_user',on_delete=models.CASCADE,default=None,blank=True,null=True)
    down_vote_by=models.ForeignKey(Account,related_name='down_vote_user',on_delete=models.CASCADE,default=None,blank=True,null=True)
    