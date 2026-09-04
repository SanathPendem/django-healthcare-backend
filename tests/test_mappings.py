"""
Tests for PatientDoctorMapping management API endpoints.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping
from patients.models import Patient
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class MappingAPITests(APITestCase):
    """Test suite for doctor-patient assignment mappings."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            name='User One',
            password='Password123!'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            name='User Two',
            password='Password123!'
        )

        self.patient1 = Patient.objects.create(
            name='Patient One',
            email='p1@example.com',
            created_by=self.user1
        )
        self.patient2 = Patient.objects.create(
            name='Patient Two',
            email='p2@example.com',
            created_by=self.user2
        )

        self.doctor1 = Doctor.objects.create(
            name='Dr. Cardia',
            email='cardia@example.com',
            specialization='Cardiology',
            created_by=self.user1
        )
        self.doctor2 = Doctor.objects.create(
            name='Dr. Neuro',
            email='neuro@example.com',
            specialization='Neurology',
            created_by=self.user1
        )

        self.list_create_url = reverse('mappings:mapping-list')

    def test_assign_doctor_to_patient_success(self):
        """User 1 assigns Doctor 1 to Patient 1 owned by User 1."""
        self.client.force_authenticate(user=self.user1)
        payload = {
            'patient': self.patient1.id,
            'doctor': self.doctor1.id,
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            PatientDoctorMapping.objects.filter(
                patient=self.patient1,
                doctor=self.doctor1
            ).exists()
        )

    def test_assign_doctor_to_unowned_patient_fails(self):
        """User 1 attempts to assign doctor to Patient 2 owned by User 2."""
        self.client.force_authenticate(user=self.user1)
        payload = {
            'patient': self.patient2.id,
            'doctor': self.doctor1.id,
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('patient', response.data)

    def test_assign_duplicate_doctor_mapping_fails(self):
        """Attempting to assign same doctor to same patient twice returns 400 Bad Request."""
        PatientDoctorMapping.objects.create(
            patient=self.patient1,
            doctor=self.doctor1,
            created_by=self.user1
        )
        self.client.force_authenticate(user=self.user1)
        payload = {
            'patient': self.patient1.id,
            'doctor': self.doctor1.id,
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_doctors_for_patient(self):
        """GET /api/mappings/<patient_id>/ returns list of doctors assigned to that patient."""
        PatientDoctorMapping.objects.create(
            patient=self.patient1,
            doctor=self.doctor1,
            created_by=self.user1
        )
        PatientDoctorMapping.objects.create(
            patient=self.patient1,
            doctor=self.doctor2,
            created_by=self.user1
        )

        self.client.force_authenticate(user=self.user1)
        detail_url = reverse('mappings:mapping-detail', kwargs={'pk': self.patient1.id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['assigned_doctors_count'], 2)

    def test_delete_mapping_success(self):
        """User 1 deletes mapping by mapping ID."""
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient1,
            doctor=self.doctor1,
            created_by=self.user1
        )
        self.client.force_authenticate(user=self.user1)
        mapping_url = reverse('mappings:mapping-detail', kwargs={'pk': mapping.id})
        response = self.client.delete(mapping_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(PatientDoctorMapping.objects.filter(id=mapping.id).exists())
