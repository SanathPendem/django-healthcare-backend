"""
Serializers for PatientDoctorMapping model.
"""

from doctors.serializers import DoctorSerializer
from patients.serializers import PatientSerializer
from rest_framework import serializers

from .models import PatientDoctorMapping


class MappingSerializer(serializers.ModelSerializer):
    """Serializer for creating and retrieving PatientDoctorMapping instances."""

    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = (
            'id',
            'patient',
            'doctor',
            'patient_detail',
            'doctor_detail',
            'created_by',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def validate(self, attrs):
        """
        Validate patient ownership and check for duplicate assignments.
        """
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        patient = attrs.get('patient')
        doctor = attrs.get('doctor')

        # Ensure user owns patient unless staff
        if user and not (user.is_staff or user.is_superuser):
            if patient.created_by != user:
                raise serializers.ValidationError({
                    'patient': 'You can only assign doctors to patients that you created/own.'
                })

        # Edge case: Check if mapping already exists
        mapping_exists = PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists()
        if mapping_exists:
            raise serializers.ValidationError({
                'non_field_errors': ['This doctor is already assigned to the specified patient.']
            })

        return attrs


class PatientDoctorsSerializer(serializers.Serializer):
    """Serializer for displaying patient information along with all assigned doctors."""

    patient = PatientSerializer()
    assigned_doctors = DoctorSerializer(many=True)
