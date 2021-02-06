from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    BasePermission,
    IsAdminUser,
)


class PermissionMixin:
    def get_permissions(self):
        permission_classes = []

        if self.action in ("list", "retrieve"):
            permission_classes = [AllowAny]

        if self.action in ("create", "destroy", "update", "partial_update"):
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class IsAuthorOrStaff(BasePermission):
    """
    Доступ для автора, модератора или администратора.
    """

    def has_object_permission(self, request, view, obj):

        return (
            request.method in SAFE_METHODS
            or request.user.role in ["admin", "moderator"]
            or obj.author == request.user
        )
