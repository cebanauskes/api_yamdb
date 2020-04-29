from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import EmailField, CharField

from .models import User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class CheckConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role', )
        model = User
