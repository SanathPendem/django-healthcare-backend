"""
Custom permissions for Mappings module.
"""

from rest_framework import permissions


class IsMappingOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission for PatientDoctorMapping.
    Ensures user owns the patient record associated with the mapping (or is staff/admin).
    """

    def has_permission(self, request, view):
        """Ensure request user is authenticated."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Check if request.user owns the patient in the mapping or is admin."""
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.patient.created_by == request.user or obj.created_by == request.user
