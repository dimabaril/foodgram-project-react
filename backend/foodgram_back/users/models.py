from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    """Our custom user model."""
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)  # ^[\w.@+-]+\z
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=150, )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

#    @property
#    def is_admin(self):
#        return self.role == self.ADMIN or self.is_staff or self.is_superuser
#
#    @property
#    def is_moderator(self):
#        return self.role == self.MODER
#
#    @property
#    def is_user(self):
#        return self.role == self.USER
