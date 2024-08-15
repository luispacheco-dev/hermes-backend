from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email Is Null')
        if password is None or password == '':
            raise ValueError('Password Is Null')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs['is_staff']     = True
        kwargs['is_active']    = True
        kwargs['is_superuser'] = True
        return self.create_superuser(email, password, **kwargs)
