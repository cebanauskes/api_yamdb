from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ParseError
from api.models import Title
from .models import Review, Comment
from .serializers import ReviewSerialier, CommentSerializer
from .permissions import IsAuthorOrAdminOrModerator
from .pagination import ReviewPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerialier
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator,)
    pagination_class = ReviewPagination 
    

    def get_queryset(self, *args, **kwargs):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(title=title, author=self.request.user).exists():
            raise ParseError
        serializer.save(author=self.request.user, title=title)
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=["rating"])

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=["rating"])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerator, )
    pagination_class = ReviewPagination

    def get_queryset(self, *args, **kwargs):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
    
    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

