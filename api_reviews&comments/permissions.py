from rest_framework import permissions


class IsAuthorOrAdminOrModeratorOrAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS or 
                request.user and request.user.is_staff or 
                request.user.role == 'admin' or 
                request.user.role == 'moderator' or 
                obj.author == request.user or
                request.method == 'POST' and request.user.is_authenticated()):
            return True
