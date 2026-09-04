"""
Views for Patient management using ModelViewSet.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Patient
from .permissions import IsPatientOwner
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for managing Patient records.
    Users can only view and manage patient records they created (unless admin).
    """

    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsPatientOwner]

    def get_queryset(self):
        """
        Filter patients list so users only see patient records they created.
        For detail actions, return all to allow object permission checks (IsPatientOwner)
        to trigger 403 Forbidden when a user accesses a patient owned by someone else.
        """
        user = self.request.user
        if self.action == 'list':
            if user.is_staff or user.is_superuser:
                return Patient.objects.all()
            return Patient.objects.filter(created_by=user)
        return Patient.objects.all()

    def perform_create(self, serializer):
        """Automatically set `created_by` to the authenticated user upon creation."""
        serializer.save(created_by=self.request.user)
