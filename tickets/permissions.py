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
    Allows access to users with the ADMIN role, or Django staff/superusers.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.role == 'ADMIN' or user.is_staff or user.is_superuser))
