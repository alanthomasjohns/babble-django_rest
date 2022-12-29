from user.models import Account
from django.db import models
from django.conf import settings


# Create your models here.

class Conversation(models.Model):
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_starter"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_participant"
    )
    start_time = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chats'
    )

    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ['-created']


class Message(models.Model):
    # Fields for the message model, such as sender, recipient, content, etc.
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, db_index=True, null=True)
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, db_index=True, related_name="reciept", null=True)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)