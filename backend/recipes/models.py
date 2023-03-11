from core.models import CommonFieldsModel, CreationDate
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.functions import Length
from sorl.thumbnail import ImageField

User = get_user_model()

models.CharField.register_lookup(Length)


class Ingredient(CommonFieldsModel):

    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=16,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'measurement_unit'),
                name='%(app_label)s_%(class)s_title_unique'
            ),
            models.CheckConstraint(
                check=models.Q(title__length__gt=0),
                name='\n%(app_label)s_%(class)s_title is empty\n',
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__length__gt=0),
                name='\n%(app_label)s_%(class)s_measurement_unit is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.title} {self.measurement_unit}'


class Recipe(CommonFieldsModel):
    author = models.ForeignKey(
        verbose_name='Автор публикации',
        related_name='recipes',
        to=User,
        on_delete=models.SET_NULL,
        null=True,
    )
    image = ImageField(
        verbose_name='Картинка',
        upload_to='recipe_images/',
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
    )
    ingredients = models.ManyToManyField(
        verbose_name='Ингредиенты',
        related_name='recipes',
        to=Ingredient,
        through='recipes.QuantityIngredients',
    )
    tags = models.ManyToManyField(
        verbose_name='Тег',
        related_name='recipes',
        to='Tag',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=0,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='%(app_label)s_%(class)s_author_unique',
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_title is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.title}. Автор: {self.author.username}'


class Tag(CommonFieldsModel):
    color_hex = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=7,
        unique=True,
    )
    slug = models.CharField(
        verbose_name='Slug',
        max_length=64,
        unique=True,
        db_index=False,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    
    def __str__(self) -> str:
        return f'{self.title} (цвет: {self.color_hex})'


class QuantityIngredients(models.Model):
    recipe = models.ForeignKey(
        verbose_name='Рецепт',
        related_name='ingredient',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        verbose_name='Ингредиент',
        related_name='recipe',
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
    )

    class Meta:
        verbose_name = 'Количество'
        verbose_name_plural = 'Количество'
        ordering = ('recipe', )
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredients'),
                name='\n%(app_label)s_%(class)s ingredient has already been added\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.quantity} {self.ingredients}'


class FavoritesList(CreationDate):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        related_name='signed',
        to=User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        verbose_name='Рецепт',
        related_name='favorites',
        to=Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='\n%(app_label)s_%(class)s recipe is already in my favorites\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'


class ShoppingList(CreationDate):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        related_name='customer',
        to=User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        verbose_name='Рецепт',
        related_name='shopping_list',
        to=Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='\n%(app_label)s_%(class)s recipe is already on the shopping list\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'
