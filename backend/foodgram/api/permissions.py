from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """Check if the user is Author or an Admin."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser
