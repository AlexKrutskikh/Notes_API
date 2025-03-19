from rest_framework import permissions

"""
   Разрешение, которое позволяет редактировать объект только владельцам или администраторам.
   """


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id or request.user.is_staff
