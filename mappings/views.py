"""
Views for PatientDoctorMapping management.
"""

from doctors.serializers import DoctorSerializer
from patients.models import Patient
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import PatientDoctorMapping
from .permissions import IsMappingOwnerOrAdmin
from .serializers import MappingSerializer


class MappingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctor-patient assignments.
    Endpoints:
    - POST /api/mappings/ : Assign doctor to patient.
    - GET /api/mappings/ : List all mappings (for owned patients).
    - GET /api/mappings/<patient_id>/ : List all doctors assigned to a specific patient.
    - DELETE /api/mappings/<id>/ : Remove a doctor-patient assignment.
    """

    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated, IsMappingOwnerOrAdmin]

    def get_queryset(self):
        """
        Filter mappings so non-staff users only see mappings
        associated with patients they created.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return PatientDoctorMapping.objects.all()
        return PatientDoctorMapping.objects.filter(patient__created_by=user)

    def perform_create(self, serializer):
        """Automatically record created_by user when creating assignment."""
        serializer.save(created_by=self.request.user)

    def retrieve(self, request, pk=None):
        """
        Retrieve mapping(s).
        Handles `GET /api/mappings/<patient_id>/` to return all doctors assigned to a patient,
        while falling back to single mapping retrieval by mapping ID if requested.
        """
        user = request.user

        # First, check if pk corresponds to a Patient ID
        patient = Patient.objects.filter(pk=pk).first()
        if patient:
            # Enforce patient ownership permission check
            if not (user.is_staff or user.is_superuser) and patient.created_by != user:
                raise PermissionDenied('You do not have permission to view mappings for this patient.')

            mappings = PatientDoctorMapping.objects.filter(patient=patient)
            serializer = self.get_serializer(mappings, many=True)
            return Response({
                'patient_id': patient.id,
                'patient_name': patient.name,
                'assigned_doctors_count': mappings.count(),
                'mappings': serializer.data,
            }, status=status.HTTP_200_OK)

        # Second, check if pk corresponds to a PatientDoctorMapping ID
        mapping = PatientDoctorMapping.objects.filter(pk=pk).first()
        if mapping:
            self.check_object_permissions(request, mapping)
            serializer = self.get_serializer(mapping)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {'detail': 'No Patient or Mapping found with the given ID.'},
            status=status.HTTP_404_NOT_FOUND
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a mapping by mapping ID.
        Ensures permission checks are enforced before deleting.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'detail': 'Patient-doctor assignment removed successfully.'},
            status=status.HTTP_200_OK
        )
