from collections import OrderedDict

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.query import QuerySet
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, QuantityIngredients, Recipe, Tag
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField)
from users.serializers import UserSerializer


class TagSerializer(ModelSerializer):
    """
    Сериализатор тэгов.
    """
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__',


class IngredientSerializer(ModelSerializer):
    """
    Сериализатор ингредиентов.
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__',


class QuantityIngredientsSerializer(ModelSerializer):
    """
    Сериализатор получения ингредиента с количеством для рецепта
    для связанных моделей.
    """
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = QuantityIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(ModelSerializer):
    """
    Сериализатор рецептов.
    """
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField(read_only=True)
    # is_favorited = SerializerMethodField()
    # is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = (
            'is_favorite',
            'is_shopping_cart',
        )

    def get_ingredients(self, obj: Recipe) -> OrderedDict:
        """Возвращает списка ингредиентов рецепта."""
        queryset = obj.qt_ingredients.all()
        return QuantityIngredientsSerializer(queryset, many=True).data

    # def get_is_favorited(self, obj: Recipe) -> bool:
    #     """
    #     Возвращает :obj:`bool` наличия рецепта в избранном.
    #     """
    #     user = self.context.get('view').request.user
    #     if user.is_anonymous:
    #         return False
    #     return user.is_favorited.filter(recipe=obj).exists()

    # def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
    #     """
    #     Возвращает :obj:`bool` наличие рецепта в списке покупок.
    #     """
    #     user = self.context.get('view').request.user
    #     if user.is_anonymous:
    #         return False
    #     return user.is_in_shopping_cart.filter(recipe=obj).exists()


class QuantityIngredientsCreateSerializer(ModelSerializer):
    """Дополнительный сериализатор рецептов для поля ingredients."""
    id = IntegerField()

    class Meta:
        model = QuantityIngredients
        fields = ('id', 'amount')


class RecipeCreateSerializer(ModelSerializer):
    """Сериализатор для создания и изменения рецептов."""
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    author = UserSerializer(read_only=True)
    id = ReadOnlyField()
    ingredients = QuantityIngredientsCreateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )

    def validate(self, obj: OrderedDict) -> OrderedDict:
        """
        Валидация тегов и ингридиентов.
        """

        for field in ['name', 'text', 'ingredients', 'tags', 'cooking_time']:
            if not obj.get(field):
                raise ValidationError(
                    f'{field} - Обязательное поле.'
                )
        ingredients = self.initial_data.get('ingredients')
        ingredients_id = tuple(i['id'] for i in ingredients)
        if len(ingredients_id) != len(set(ingredients_id)):
            raise ValidationError(
                'Ингредиенты должны быть уникальны.'
            )
        obj.update({
            'author': self.context.get('request').user
        })
        return obj

    @transaction.atomic
    def __create_update_recipe(self,
                               recipe: QuerySet(Recipe),
                               ingredients: dict,
                               tags: list) -> None:
        """
        Создаёт экземпляры класса QuantityIngredients
        связанных моделей Recipe и Ingredients и связывает
        Recipe с Tags.
        """
        recipe.tags.set(tags)
        objs = tuple(
            QuantityIngredients(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=ingredient['id']),
                amount=ingredient['amount'])
            for ingredient in ingredients
        )
        QuantityIngredients.objects.bulk_create(objs)

    @transaction.atomic
    def create(self, validated_data):
        """
        Создает рецепт и сохраняет его в базе данных.
        """
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.__create_update_recipe(recipe, ingredients, tags)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Обновляет рецепт и сохраняет его в базе данных.
        """
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)

        QuantityIngredients.objects.filter(
            recipe=instance,
            ingredient__in=instance.ingredients.all()
        ).delete()

        self.__create_update_recipe(instance, ingredients, tags)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data
