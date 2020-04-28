from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    )

    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default='user',
    )

    description = models.TextField(max_length=500, blank=True)
