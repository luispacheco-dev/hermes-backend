from django.db import models
from xfriend.models import Friend
from xprofile.models import Profile


class Chat(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)

    def __str__(self):
        return "Chat " + self.friend


class Message(models.Model):
    content = models.CharField(max_length=254)
    readed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
