from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверка доступа только для владельца объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
