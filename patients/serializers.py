"""
Serializers for Patient model CRUD operations.
"""

from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model including creation and detail representation."""

    created_by_email = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = Patient
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'medical_history',
            'created_by',
            'created_by_email',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_by_email', 'created_at', 'updated_at')

    def validate_name(self, value):
        """Ensure patient name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError('Patient name cannot be empty.')
        return value.strip()
