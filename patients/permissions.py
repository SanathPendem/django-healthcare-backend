"""
Custom permissions for Patients module.
"""

from rest_framework import permissions


class IsPatientOwner(permissions.BasePermission):
    """
    Custom permission to ensure users can only view and manage
    their own patient records unless they are admin/staff.
    """

    def has_permission(self, request, view):
        """Ensure user is authenticated for any action."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Check if request.user is creator of the patient record or an admin."""
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.created_by == request.user
