"""
Tests for authentication endpoints (Registration & Login).
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTests(APITestCase):
    """Test suite for user registration and JWT login endpoints."""

    def setUp(self):
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.valid_payload = {
            'name': 'Dr. Alice Smith',
            'email': 'alice@example.com',
            'password': 'SecurePassword123!',
        }

    def test_register_user_success(self):
        """Test successful registration returns user data and JWT tokens."""
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertEqual(response.data['user']['email'], 'alice@example.com')
        self.assertEqual(response.data['user']['name'], 'Dr. Alice Smith')
        self.assertTrue(User.objects.filter(email='alice@example.com').exists())

    def test_register_duplicate_email(self):
        """Test registration fails with 400 Bad Request when email already exists."""
        User.objects.create_user(
            email='alice@example.com',
            name='Alice Smith',
            password='SecurePassword123!'
        )
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_weak_password(self):
        """Test registration fails when password is less than 8 characters."""
        weak_payload = {
            'name': 'Short Password User',
            'email': 'short@example.com',
            'password': '123',
        }
        response = self.client.post(self.register_url, weak_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login_user_success(self):
        """Test logging in with valid credentials returns JWT tokens."""
        User.objects.create_user(
            email='alice@example.com',
            name='Alice Smith',
            password='SecurePassword123!'
        )
        login_payload = {
            'email': 'alice@example.com',
            'password': 'SecurePassword123!',
        }
        response = self.client.post(self.login_url, login_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

    def test_login_invalid_password(self):
        """Test login fails with incorrect password."""
        User.objects.create_user(
            email='alice@example.com',
            name='Alice Smith',
            password='SecurePassword123!'
        )
        invalid_payload = {
            'email': 'alice@example.com',
            'password': 'WrongPassword!',
        }
        response = self.client.post(self.login_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        """Test login fails for email that is not registered."""
        invalid_payload = {
            'email': 'nobody@example.com',
            'password': 'SecurePassword123!',
        }
        response = self.client.post(self.login_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
