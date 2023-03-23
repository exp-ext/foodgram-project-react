import json

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.routers import DefaultRouter
from rest_framework.test import APIClient, APITestCase

from ..models import (FavoritesList, Ingredient, IngredientsInRecipe, Recipe,
                      ShoppingList, Tag)
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
        self.user_client = APIClient()
        self.user_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user.key
        )
        self.author_client = APIClient()
        self.author_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_author.key
        )
        self.not_auth_client = APIClient()

        router.register('recipes', RecipeViewSet, basename='tags')

        self.recipe = Recipe.objects.create(**self.recipe_data)
        IngredientsInRecipe.objects.create(
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
        url = reverse('recipes:recipes-list')
        response = self.author_client.post(
            url, self.new_recipe_data, format='json'
        )
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

    def test_create_recipe_not_auth(self):
        """
        Тест на создание рецепта не авторизованным пользователем.
        """
        url = reverse('recipes:recipes-list')
        response = self.not_auth_client.post(
            url, self.new_recipe_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_recipe_with_wrong_ingredients(self):
        """
        Тест на создание рецепта с не уникальными ингридиентами.
        """
        url = reverse('recipes:recipes-list')
        wrong_data = self.new_recipe_data
        wrong_data['ingredients'] = [
            {'id': 1, 'amount': 5}, {'id': 1, 'amount': 2}
        ]
        response = self.author_client.post(url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            ('Ингредиенты должны быть уникальны.'
                in response.data['ingredients'])
        )

    def test_create_recipe_with_wrong_tag(self):
        """
        Тест на создание рецепта с не существующим тегом.
        """
        url = reverse('recipes:recipes-list')
        wrong_data = self.new_recipe_data
        wrong_data['tags'] = [5, 100]
        response = self.author_client.post(url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_with_blank_ingredients(self):
        """
        Тест на создание рецепта с пустым ингридиентом.
        """
        url = reverse('recipes:recipes-list')
        wrong_data = self.new_recipe_data
        wrong_data['ingredients'] = {'id': '', 'amount': ''}
        response = self.author_client.post(url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_with_blank_name(self):
        """
        Тест на создание рецепта с пустым названием.
        """
        url = reverse('recipes:recipes-list')
        wrong_data = self.new_recipe_data
        field = 'name'
        wrong_data[field] = ''
        response = self.author_client.post(url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('Обязательное поле.' in response.data[field])

    def test_create_recipe_with_missing_cooking_time(self):
        """
        Тест на создание рецепта с отсутствующим cooking_time.
        """
        url = reverse('recipes:recipes-list')
        wrong_data = self.new_recipe_data
        field = 'cooking_time'
        wrong_data.pop(field)
        response = self.author_client.post(url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('Обязательное поле.' in response.data[field])

    def test_create_recipe_with_blank_tags(self):
        """
        Тест на создание рецепта с пустым тегом.
        """
        url = reverse('recipes:recipes-list')
        wrong_data = self.new_recipe_data
        wrong_data['tags'] = []
        response = self.author_client.post(url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_recipe(self):
        """
        Тест на изменение рецепта.
        """
        url = f'/api/recipes/{self.recipe.pk}/'
        response = self.author_client.patch(
            url, self.new_recipe_data, format='json'
        )
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

    def test_delete_recipe(self):
        """
        Тест на удаление рецепта.
        """
        url = reverse('recipes:recipes-detail', args=[self.recipe.pk])
        response = self.not_auth_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.author_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.author_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_recipe(self):
        """
        Тест получения списка рецептов.
        """
        url = reverse('recipes:recipes-list')
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        result = response.data.get('results')
        self.assertEqual(result[0].get('name'), self.recipe.name)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_recipe(self):
        """
        Тест получения рецепта по id.
        """
        url = reverse('recipes:recipes-detail', args=[self.recipe.pk])
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.recipe.name)
        self.assertEqual(len(response.data), 10)

    def test_favorite_create_destroy(self):
        """
        Тест на добавление и удаление из избранного.
        """
        start_count = FavoritesList.objects.count()
        url = f'/api/recipes/{self.recipe.pk}/favorite/'
        response = self.not_auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.user_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoritesList.objects.count(), start_count + 1)
        recipe = Recipe.objects.get(id=self.recipe.pk)
        self.assertTrue(FavoritesList.objects.filter(
            user=self.user,
            recipe=recipe
        ).exists())
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.get('id'), self.recipe.pk)
        self.assertEqual(response.get('name'), self.recipe.name)
        self.assertEqual(
            response.get('cooking_time'), self.recipe.cooking_time
        )
        response = self.user_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.user_client.delete(url)
        self.assertEqual(FavoritesList.objects.count(), start_count)

    def test_shopping_cart_create_destroy(self):
        """
        Тест на добавление и удаление из корзины.
        """
        start_count = ShoppingList.objects.count()
        url = f'/api/recipes/{self.recipe.pk}/shopping_cart/'
        response = self.not_auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.user_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShoppingList.objects.count(), start_count + 1)
        recipe = Recipe.objects.get(id=self.recipe.pk)
        self.assertTrue(ShoppingList.objects.filter(
            user=self.user,
            recipe=recipe
        ).exists())
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.get('id'), self.recipe.pk)
        self.assertEqual(response.get('name'), self.recipe.name)
        self.assertEqual(
            response.get('cooking_time'), self.recipe.cooking_time
        )
        response = self.user_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.user_client.delete(url)
        self.assertEqual(ShoppingList.objects.count(), start_count)

    def test_shopping_cart_get_file(self):
        """
        Тест на получение списка покупок.
        """
        url = '/api/recipes/download_shopping_cart/'
        response = self.not_auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
