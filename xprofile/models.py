from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email
