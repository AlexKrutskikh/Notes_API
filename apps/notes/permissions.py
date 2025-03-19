from rest_framework import permissions

from apps.auth.models import User

"""Разрешение, которое позволяет редактировать объект только владельцам или администраторам."""


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id or request.user.is_staff


"""Разрешение, которое запрещает действия с ролью Editor"""


class EditorReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            user = User.objects.get(id=request.user.id)
            role = user.role
        except User.DoesNotExist:
            return False

        return role != "Editor"
