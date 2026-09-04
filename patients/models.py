"""
Patient model definition for Healthcare Backend.
"""

from django.conf import settings
from django.db import models


class Patient(models.Model):
    """
    Patient model representing healthcare patients.
    Each patient is owned by the user (`created_by`) who added them.
    """

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    name = models.CharField('Full Name', max_length=255)
    email = models.EmailField('Email Address')
    phone = models.CharField('Phone Number', max_length=20, blank=True, default='')
    date_of_birth = models.DateField('Date of Birth', null=True, blank=True)
    gender = models.CharField('Gender', max_length=20, choices=GENDER_CHOICES, default='Other')
    medical_history = models.TextField('Medical History', blank=True, default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patients',
        verbose_name='Created By'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']

    def __str__(self):
        return f"Patient: {self.name} ({self.email})"
