from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    bio = models.TextField(max_length=300, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class UserRole(models.TextChoices):
        user = 'user'
        moderator = 'moderator'
        admin = 'admin'

    role = models.CharField(
        max_length=9,
        choices=UserRole.choices,
        default=UserRole.user,
    )

    objects = CustomUserManager()


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=300)
    year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Категория')
