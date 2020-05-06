from rest_framework import serializers
from .models import Review


class ReviewSerialier(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review
        