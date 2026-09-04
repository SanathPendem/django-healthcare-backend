"""
Doctor model definition for Healthcare Backend.
"""

from django.conf import settings
from django.db import models


class Doctor(models.Model):
    """
    Doctor model representing medical practitioners.
    Doctors are viewable by all authenticated users, but modified only by creator or admin.
    """

    name = models.CharField('Full Name', max_length=255)
    email = models.EmailField('Email Address', unique=True)
    phone = models.CharField('Phone Number', max_length=20, blank=True, default='')
    specialization = models.CharField('Specialization', max_length=150)
    experience_years = models.PositiveIntegerField('Years of Experience', default=0)
    hospital_affiliation = models.CharField('Hospital Affiliation', max_length=255, blank=True, default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctors',
        verbose_name='Created By'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        ordering = ['-created_at']

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
