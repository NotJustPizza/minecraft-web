from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password = models.NOT_PROVIDED

    objects = UserManager()

    USERNAME_FIELD = 'uuid'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['uuid', "name"]

    def get_full_name(self):
        full_name = '%s %s' % (self.uuid, self.name)
        return full_name.strip()

    def get_short_name(self):
        return self.name


class Item(models.Model):
    type = models.PositiveSmallIntegerField()
    meta = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=256)
    displayName = models.CharField(max_length=256)
    breakable = models.BooleanField()
    stack_type = models.PositiveSmallIntegerField(
        choices=[
            (1, 'non_stackable'),
            (16, 'special'),
            (64, 'stackable')
        ],
        default=1
    )
