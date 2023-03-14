from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from ..models import Ingredient

User = get_user_model()


class IngredientViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass', is_staff=True
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client = APIClient()

        self.ingredient1 = Ingredient.objects.create(
            name='ingredient1',
            measurement_unit='unit',
        )
        self.ingredient2 = Ingredient.objects.create(
            name='ingredient2',
            measurement_unit='unit',
        )

    def test_list_ingredients(self):
        url = reverse('recipes:ingredients-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_ingredient(self):
        url = reverse('recipes:ingredients-detail', args=[self.ingredient1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.ingredient1.name)
