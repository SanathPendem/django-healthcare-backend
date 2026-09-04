"""
Tests for Patient management API endpoints.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from patients.models import Patient
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class PatientAPITests(APITestCase):
    """Test suite for Patient CRUD operations and permissions."""

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
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            name='Admin User',
            password='Password123!'
        )

        self.patient1 = Patient.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            gender='Male',
            medical_history='Hypertension',
            created_by=self.user1
        )

        self.list_create_url = reverse('patients:patient-list')
        self.detail_url_p1 = reverse('patients:patient-detail', kwargs={'pk': self.patient1.pk})

    def test_unauthenticated_request_fails(self):
        """Unauthenticated user receives 401 Unauthorized."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_patient_success(self):
        """Authenticated user creates patient successfully."""
        self.client.force_authenticate(user=self.user1)
        payload = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '9876543210',
            'gender': 'Female',
            'medical_history': 'Diabetes'
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Jane Doe')
        self.assertEqual(response.data['created_by_email'], self.user1.email)

    def test_list_patients_user_isolation(self):
        """User 1 only sees patients created by User 1."""
        Patient.objects.create(
            name='Patient of User 2',
            email='p2@example.com',
            created_by=self.user2
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_retrieve_patient_owner_success(self):
        """Patient owner can retrieve patient details."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.detail_url_p1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_retrieve_patient_non_owner_forbidden(self):
        """Non-owner user receives 403 Forbidden when accessing patient detail."""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.detail_url_p1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_patient_owner_success(self):
        """Patient owner can update patient record."""
        self.client.force_authenticate(user=self.user1)
        payload = {'name': 'John Updated'}
        response = self.client.patch(self.detail_url_p1, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient1.refresh_from_db()
        self.assertEqual(self.patient1.name, 'John Updated')

    def test_delete_patient_non_owner_forbidden(self):
        """Non-owner user receives 403 Forbidden on delete attempt."""
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.detail_url_p1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_and_delete_any_patient(self):
        """Admin can access and delete any patient."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url_p1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(pk=self.patient1.pk).exists())
