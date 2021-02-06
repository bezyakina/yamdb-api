from rest_framework import permissions

from .models import UserRole


class IsAdminOrSuperUser(permissions.BasePermission):
    """Права доступа для администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
