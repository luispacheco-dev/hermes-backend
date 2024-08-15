from django.db import models
from django.utils import timezone
from .utils import get_upload_path
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


class Profile(models.Model):
    logged = models.BooleanField(default=False)
    picture = models.ImageField(upload_to=get_upload_path, null=True)

    last_name = models.CharField(max_length=254)
    first_name = models.CharField(max_length=254)

    username = models.TextField(max_length=600)
    last_login = models.DateTimeField(null=True)

    code = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__previuos_logged_state = self.logged
        self.__previuos_last_name = self.last_name
        self.__previus_first_name = self.first_name

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.logged != self.__previuos_logged_state:
            self.last_login = timezone.now()
            self.__previuos_logged_state = self.logged
        if self.first_name != self.__previus_first_name or self.last_name != self.__previuos_last_name:
            self.username = f"{self.first_name} {self.last_name}"
            self.__previuos_last_name = self.last_name
            self.__previus_first_name = self.first_name
        return super(Profile, self).save(*args, **kwargs)
