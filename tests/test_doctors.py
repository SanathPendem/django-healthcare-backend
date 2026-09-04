"""
Tests for Doctor management API endpoints.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from doctors.models import Doctor
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class DoctorAPITests(APITestCase):
    """Test suite for Doctor CRUD operations and permission rules."""

    def setUp(self):
        self.creator = User.objects.create_user(
            email='creator@example.com',
            name='Creator User',
            password='Password123!'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            name='Other User',
            password='Password123!'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            name='Admin User',
            password='Password123!'
        )

        self.doctor = Doctor.objects.create(
            name='Dr. Gregory House',
            email='house@diagnostics.org',
            phone='555-0199',
            specialization='Diagnostic Medicine',
            experience_years=15,
            hospital_affiliation='Princeton-Plainsboro',
            created_by=self.creator
        )

        self.list_create_url = reverse('doctors:doctor-list')
        self.detail_url = reverse('doctors:doctor-detail', kwargs={'pk': self.doctor.pk})

    def test_unauthenticated_request_fails(self):
        """Unauthenticated user receives 401 Unauthorized."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_authenticated_users_can_list_doctors(self):
        """Any authenticated user can list all doctors."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_all_authenticated_users_can_retrieve_doctor_detail(self):
        """Any authenticated user can retrieve single doctor details."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Dr. Gregory House')

    def test_create_doctor_success(self):
        """Authenticated user creates doctor successfully."""
        self.client.force_authenticate(user=self.other_user)
        payload = {
            'name': 'Dr. Meredith Grey',
            'email': 'grey@grey-sloan.org',
            'specialization': 'General Surgery',
            'experience_years': 10,
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_by_email'], self.other_user.email)

    def test_update_doctor_non_creator_forbidden(self):
        """Non-creator user receives 403 Forbidden when updating doctor."""
        self.client.force_authenticate(user=self.other_user)
        payload = {'specialization': 'Neurology'}
        response = self.client.patch(self.detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_doctor_creator_success(self):
        """Creator can delete their created doctor record."""
        self.client.force_authenticate(user=self.creator)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(pk=self.doctor.pk).exists())
