"""
PatientDoctorMapping model definition for Healthcare Backend.
"""

from django.conf import settings
from django.db import models
from doctors.models import Doctor
from patients.models import Patient


class PatientDoctorMapping(models.Model):
    """
    Model establishing many-to-many relationship mapping between Patients and Doctors.
    """

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='doctor_mappings',
        verbose_name='Patient'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='patient_mappings',
        verbose_name='Doctor'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mappings',
        verbose_name='Created By'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Patient-Doctor Mapping'
        verbose_name_plural = 'Patient-Doctor Mappings'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'doctor'],
                name='unique_patient_doctor_mapping'
            )
        ]

    def __str__(self):
        return f"Mapping: Patient '{self.patient.name}' -> Dr. '{self.doctor.name}'"
