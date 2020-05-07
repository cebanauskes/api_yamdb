from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')


class IsAdminOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.is_superuser or
                        request.user.role == 'admin')
        else:
            return True
