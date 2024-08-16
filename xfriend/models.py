from django.db import models
from xprofile.models import Profile


class Friend(models.Model):
    began_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')

    def __str__(self):
        return self.sender.user.email + ' + ' + self.receiver.user.email


class FriendRequest(models.Model):
    code = models.CharField(max_length=8)
    greetings = models.CharField(max_length=254)
    requested_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.sender.user.email + ' + ' + self.code
