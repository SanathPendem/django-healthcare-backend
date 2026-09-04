"""
Custom permissions for Doctors module.
"""

from rest_framework import permissions


class IsDoctorCreatorOrAdmin(permissions.BasePermission):
    """
    Custom permission for Doctors.
    - All authenticated users can view doctors (SAFE_METHODS).
    - Any authenticated user can create a doctor.
    - Only the user who created the doctor or an admin can update or delete it.
    """

    def has_permission(self, request, view):
        """Ensure request is authenticated."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Allow read access to any authenticated user; restrict mutations to creator or admin."""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.created_by == request.user
