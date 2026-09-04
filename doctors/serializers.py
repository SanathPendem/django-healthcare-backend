"""
Serializers for Doctor model CRUD operations.
"""

from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model including detail representation and validation."""

    created_by_email = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = Doctor
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'specialization',
            'experience_years',
            'hospital_affiliation',
            'created_by',
            'created_by_email',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_by_email', 'created_at', 'updated_at')

    def validate_name(self, value):
        """Validate doctor name is not blank."""
        if not value or not value.strip():
            raise serializers.ValidationError('Doctor name cannot be empty.')
        return value.strip()

    def validate_specialization(self, value):
        """Validate specialization is provided."""
        if not value or not value.strip():
            raise serializers.ValidationError('Specialization is required.')
        return value.strip()
