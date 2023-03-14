from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_get_token(self):
        """
        Test getting an authentication token
        """
        response = self.client.post('/api/auth/token/login/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('auth_token' in response.data)

    def test_get_user_profile(self):
        """
        Test getting user profile
        """
        response = self.client.get(
            f'/api/users/{self.user.id}/', HTTP_AUTHORIZATION=(
                f'Token {self.token.key}')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_get_current_user(self):
        """
        Test getting current user
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_set_password(self):
        """
        Test setting user password
        """
        self.client.force_authenticate(user=self.user)
        new_password_data = {
            'new_password': 'newtestpassword',
            're_new_password': 'newtestpassword'
        }
        response = self.client.post(
            '/api/users/set_password/', new_password_data
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.user.check_password(
            new_password_data['new_password'])
        )

    def test_logout(self):
        """
        Test logging out and invalidating token
        """
        response = self.client.post(
            '/api/auth/token/logout/', HTTP_AUTHORIZATION=(
                f'Token {self.token.key}')
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=self.user).exists())
