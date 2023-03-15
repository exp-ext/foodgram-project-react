from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import AuthorSubscription

User = get_user_model()


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'first_name': 'testuser_first_name',
            'last_name': 'testuser_last_name',
            'email': 'testuser@test.com',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_get_user_profile(self):
        """
        Тест получения профиля пользователя.
        """
        response = self.client.get(
            f'/api/users/{self.user.id}/',
            HTTP_AUTHORIZATION=(f'Token {self.token.key}')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_get_current_user(self):
        """
        Тест получения текущего пользователя.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_set_password(self):
        """
        Проверка изменения пароля пользователя.
        """
        self.client.force_authenticate(user=self.user)
        new_password_data = {
            'new_password': 'newtestpassword1',
            'current_password': 'testpassword'
        }
        response = self.client.post(
            '/api/users/set_password/', new_password_data
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            self.user.check_password(new_password_data['current_password'])
        )
        self.assertTrue(
            self.user.check_password(new_password_data['new_password'])
        )

    def test_get_publisher(self):
        """
        Проверка получения авторов, на которых подписан текущий пользователь.
        """
        response = self.client.get(
            '/api/users/subscriptions/',
            HTTP_AUTHORIZATION=(f'Token {self.token.key}')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_unfolow(self):
        """
        Проверка подписки и отписки от авторов.
        """
        author_data = {
            'id': 2,
            'username': 'testauthor',
            'first_name': 'testauthor_first_name',
            'last_name': 'testauthor_last_name',
            'email': 'testauthor@test.com',
            'password': 'authorpassword'
        }
        start_follow_count = AuthorSubscription.objects.count()
        User.objects.create_user(**author_data)
        response = self.client.post(
            '/api/users/2/subscribe/',
            HTTP_AUTHORIZATION=(f'Token {self.token.key}')
        )
        self.assertEquals(AuthorSubscription.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(
            '/api/users/2/subscribe/',
            HTTP_AUTHORIZATION=(f'Token {self.token.key}')
        )
        self.assertEquals(
            AuthorSubscription.objects.count(),
            start_follow_count
        )
