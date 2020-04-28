from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework.serializers import EmailField, CharField

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = EmailField(
        max_length=50,
        validators=[UniqueValidator(queryset=User.objects.all())],
        allow_blank=False
    )

    username = CharField(
        max_length=40,
        validators=[UniqueValidator(queryset=User.objects.all())],
        allow_blank=False
    )

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role', )
        model = User
