from .models import Message, Conversation
from django.contrib import admin

# Register your models here.
admin.site.register([Message, Conversation])