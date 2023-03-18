from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.routers import DefaultRouter
from rest_framework.test import APITestCase

from ..models import Ingredient, QuantityIngredients, Recipe, Tag
from ..views import RecipeViewSet

router = DefaultRouter()

User = get_user_model()

IMAGE = (
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA'
    'AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxA'
    'GVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='
)


class TagsTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_data = {
            'username': 'testauthor_re',
            'first_name': 'testauthor_re_first_name',
            'last_name': 'testauthor_re_last_name',
            'email': 'testauthor_re@test.com',
            'password': 'testpassword'
        }
        cls.user_data = {
            'username': 'testuser_re',
            'first_name': 'testuser_re_first_name',
            'last_name': 'testuser_re_last_name',
            'email': 'testuser_re@test.com',
            'password': 'testpassword'
        }
        cls.author = User.objects.create_user(**cls.author_data)
        cls.user = User.objects.create_user(**cls.user_data)

        cls.token_author = Token.objects.create(user=cls.author)
        cls.token_user = Token.objects.create(user=cls.user)

        cls.ingredient1 = Ingredient.objects.create(
            name='ingredient1',
            measurement_unit='тн',
        )
        cls.ingredient2 = Ingredient.objects.create(
            name='ingredient2',
            measurement_unit='м3',
        )
        cls.tag1 = Tag.objects.create(
            name='tag1',
            color='#E26C2D',
            slug='tag1'
        )
        cls.tag2 = Tag.objects.create(
            name='tag2',
            color='#E40C2D',
            slug='tag2'
        )
        cls.recipe_data = {
            'name': 'тестовое имя',
            'author': cls.author,
            'image': IMAGE,
            'text': 'Некий текст',
            'cooking_time': 10
        }

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user.key
        )
        router.register('recipes', RecipeViewSet, basename='tags')

        self.recipe = Recipe.objects.create(**self.recipe_data)
        QuantityIngredients.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient1,
            amount=10
        )
        self.recipe.tags.add(self.tag1)
        self.new_recipe_data = {
            'name': 'new recipe',
            'author': {
                'email': self.author.email,
                'id': self.author.id,
                'username': self.author.username,
                'first_name': self.author.first_name,
                'last_name': self.author.last_name,
                'is_subscribed': False,
                },
            'image': IMAGE,
            'text': 'New recipe text',
            'cooking_time': 15,
            'ingredients': [
                {'id': self.ingredient1.id, 'amount': 5},
                {'id': self.ingredient2.id, 'amount': 2},
            ],
            'tags': [self.tag1.id, self.tag2.id]
        }

    def test_create_nonunique_recipe(self):
        """
        Тест на уникальность полей.
        """
        with self.assertRaises(IntegrityError):
            Recipe.objects.create(**self.recipe_data)

    def test_create_recipe(self):
        """
        Тест на создание рецепта.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_author.key
        )
        url = reverse('recipes:recipes-list')
        response = self.client.post(url, self.new_recipe_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)
        recipe = Recipe.objects.get(name='new recipe')
        self.assertEqual(recipe.author, self.author)
        self.assertEqual(recipe.text, 'New recipe text')
        self.assertEqual(recipe.cooking_time, 15)
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertEqual(recipe.tags.count(), 2)
        self.assertEqual(recipe.ingredients.first(), self.ingredient1)
        self.assertEqual(recipe.ingredients.last(), self.ingredient2)
        self.assertEqual(recipe.tags.first(), self.tag1)
        self.assertEqual(recipe.tags.last(), self.tag2)

    def test_update_recipe(self):
        """
        Тест на изменение рецепта.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_author.key
        )
        url = f'/api/recipes/{self.recipe.pk}/'
        response = self.client.patch(url, self.new_recipe_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.count(), 1)
        recipe = Recipe.objects.get(name='new recipe')
        self.assertEqual(recipe.author, self.author)
        self.assertEqual(recipe.text, 'New recipe text')
        self.assertEqual(recipe.cooking_time, 15)
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertEqual(recipe.tags.count(), 2)
        self.assertEqual(recipe.ingredients.first(), self.ingredient1)
        self.assertEqual(recipe.ingredients.last(), self.ingredient2)
        self.assertEqual(recipe.tags.first(), self.tag1)
        self.assertEqual(recipe.tags.last(), self.tag2)

    def test_list_recipe(self):
        """
        Тест получения списка рецептов.
        """
        url = reverse('recipes:recipes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        result = response.data.get('results')
        self.assertEqual(result[0].get('name'), self.recipe.name)

    def test_retrieve_tag(self):
        """
        Тест получения тега по id.
        """
        url = reverse('recipes:recipes-detail', args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.recipe.name)
