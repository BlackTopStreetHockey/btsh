from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):
    """Allows all read only operations by default."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
