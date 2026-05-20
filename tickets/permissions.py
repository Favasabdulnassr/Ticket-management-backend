from rest_framework import permissions

class IsTicketOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `created_by`.
        return obj.created_by == request.user

class IsAdminRole(permissions.BasePermission):
    """
    Allows access only to users with the ADMIN role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')
