from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpassword'
        }

    def test_create_user(self):
        """
        Test creating a new user
        """
        response = self.client.post('/api/users/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(username=self.user_data['username']).exists()
        )

    def test_create_user_invalid_data(self):
        """
        Test that creating a user with invalid data fails
        """
        invalid_user_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password': 'testpassword'
        }
        response = self.client.post('/api/users/', invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            User.objects.filter(
                username=invalid_user_data['username']).exists()
        )
