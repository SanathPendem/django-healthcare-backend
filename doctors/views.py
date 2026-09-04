"""
Views for Doctor management using ModelViewSet.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Doctor
from .permissions import IsDoctorCreatorOrAdmin
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for managing Doctor directory records.
    All authenticated users can list and view doctor details.
    Only creators or admins can update or delete a doctor record.
    """

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsDoctorCreatorOrAdmin]

    def perform_create(self, serializer):
        """Automatically associate created_by with the authenticated user."""
        serializer.save(created_by=self.request.user)
