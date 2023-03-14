from core.permissions import IsAdmin, IsOwner, ReadOnly
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientSearchFilter
from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    """
    Теги:
    - `GET` список тегов
    - `GET` получение тега

    Создание и редактирование тэгов разрешено только админам.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdmin | ReadOnly,)


class IngredientViewSet(ModelViewSet):
    """
    Ингредиенты:
    - `GET` cписок ингредиентов с возможностью поиска по имени
    - `GET` получение ингредиента
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name', )


class RecipeViewSet(ModelViewSet):
    """
    Рецепты:
    - `GET` cписок рецептов (страница доступна всем пользователям.
    Доступна фильтрация по избранному, автору, списку покупок и тегам.)
    - `POST` cоздание рецепта (доступно только авторизованному пользователю)
    - `GET` получение рецепта
    - `PATCH` oбновление рецепта (доступно только автору данного рецепта)
    - `DELETE` удаление рецепта (доступно только автору данного рецепта)
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwner | IsAdmin | ReadOnly,)
