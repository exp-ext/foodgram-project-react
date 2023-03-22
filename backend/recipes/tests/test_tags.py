from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.routers import DefaultRouter
from rest_framework.test import APITestCase

from ..models import Tag
from ..views import TagViewSet

router = DefaultRouter()


User = get_user_model()


class TagsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.tag1 = Tag.objects.create(
            name='tag1',
            color='#E26C2D',
            slug='tag1'
        )
        self.tag2 = Tag.objects.create(
            name='tag2',
            color='#E40C2D',
            slug='tag2'
        )
        router.register('tags', TagViewSet, basename='tags')

    def test_create_nonunique_tags(self):
        """
        Тест на создание неуникального поля name.
        """
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='tag1', color='#E42C2D', slug='test2')

    def test_list_tags(self):
        """
        Тест получения списка тегов.
        """
        url = reverse('recipes:tags-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)
        result = response.data.get('results')
        self.assertEqual(result[0].get('name'), self.tag1.name)
        self.assertEqual(result[1].get('name'), self.tag2.name)

    def test_retrieve_tag(self):
        """
        Тест получения тега по id.
        """
        url = reverse('recipes:tags-detail', args=[self.tag1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.tag1.name)

    def test_retrieve_wrong_tag(self):
        """
        Тест получения тега по неверному id.
        """
        url = reverse('recipes:tags-detail', args=(100,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
