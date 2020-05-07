from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from .models import Review, Title
from .serializers import ReviewSerialier
from .permissions import IsAuthorOrAdminOrModeratorOrAuthenticatedOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerialier

    def get_queryset(self, *args, **kwargs):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)



    # permission_classes = (IsAuthorOrAdminOrModeratorOrAuthenticatedOrReadOnly,)
    # queryset = Review.objects.all()