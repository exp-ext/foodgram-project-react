from core.models import CommonFieldsModel, CreationDate
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.db.models.functions import Length
from django.utils.translation import gettext_lazy as _
from pytils.translit import slugify
from sorl.thumbnail import ImageField

User = get_user_model()

models.CharField.register_lookup(Length)


class Tag(models.Model):

    name = models.CharField(
        verbose_name=_('Название'),
        max_length=256,
        unique=True,
    )
    color = models.CharField(
        verbose_name=_('Цветовой HEX-код'),
        max_length=7,
        null=False,
        unique=True,
    )
    slug = models.CharField(
        verbose_name=_('Slug'),
        max_length=64,
        unique=True,
        db_index=False,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return f'{self.name} (цвет: {self.color})'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:20]
        super().save(*args, **kwargs)


class Ingredient(CommonFieldsModel):

    measurement_unit = models.CharField(
        verbose_name=_('Единицы измерения'),
        max_length=16,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit',),
                name='%(app_label)s_%(class)s_name_unique'
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__length__gt=0),
                name='\n%(app_label)s_%(class)s_measurement_unit is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name} {self.measurement_unit}'


class Recipe(CommonFieldsModel):

    author = models.ForeignKey(
        verbose_name=_('Автор публикации'),
        related_name='recipes',
        to=User,
        on_delete=models.SET_NULL,
        null=True,
    )
    image = ImageField(
        verbose_name=_('Картинка'),
        upload_to='recipe_images/',
    )
    text = models.TextField(
        verbose_name=_('Текстовое описание'),
    )
    ingredients = models.ManyToManyField(
        verbose_name=_('Ингредиенты'),
        to=Ingredient,
        through='recipes.IngredientsInRecipe',
        through_fields=('recipe', 'ingredient'),
    )
    tags = models.ManyToManyField(
        verbose_name=_('Теги'),
        to=Tag,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name=_('Время приготовления'),
        default=0,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='%(app_label)s_%(class)s_author_unique',
            ),
            models.CheckConstraint(
                check=~Q(cooking_time=0),
                name='%(app_label)s_%(class)s_cooking_time_not_zero',
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}. Автор: {self.author.username}'


class IngredientsInRecipe(models.Model):

    recipe = models.ForeignKey(
        verbose_name=_('Рецепт'),
        related_name='qt_ingredients',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        verbose_name=_('Ингредиент'),
        related_name='qt_recipes',
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name=_('Количество'),
        default=0,
    )

    class Meta:
        verbose_name = 'Количество'
        verbose_name_plural = 'Количество'
        ordering = ('recipe', )
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name=('\n%(app_label)s_%(class)s '
                      'ingredient has already been added\n'),
            ),
        )

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredient}'


class FavoritesList(CreationDate):

    user = models.ForeignKey(
        verbose_name=_('Пользователь'),
        related_name='signed',
        to=User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        verbose_name=_('Рецепт'),
        related_name='is_favorited',
        to=Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name=('\n%(app_label)s_%(class)s '
                      'recipe is already in my favorites\n'),
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'


class ShoppingList(CreationDate):

    user = models.ForeignKey(
        verbose_name=_('Пользователь'),
        related_name='customer',
        to=User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        verbose_name=_('Рецепт'),
        related_name='is_in_shopping_cart',
        to=Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name=('\n%(app_label)s_%(class)s '
                      'recipe is already on the shopping list\n'),
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'
