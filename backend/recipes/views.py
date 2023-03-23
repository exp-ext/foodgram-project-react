import weasyprint
from core.permissions import IsAdmin, IsOwner, ReadOnly
from core.serializers import CroppedRecipeSerializer
from django.conf import settings
from django.db.models import Prefetch, Sum
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import FavoritesList, Ingredient, Recipe, ShoppingList, Tag
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, TagSerializer)


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
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    Ингредиенты:
    - `GET` cписок ингредиентов с возможностью поиска по имени
    - `GET` получение ингредиента
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdmin | ReadOnly,)
    filterset_class = IngredientFilter
    pagination_class = None


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
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated,))
    def favorite(self, request: HttpRequest, pk: str = None):
        method = 'favorite'
        return self.__del_add(FavoritesList, request, pk, method)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request: HttpRequest, pk: str = None):
        method = 'shopping_cart'
        return self.__del_add(ShoppingList, request, pk, method)

    def __del_add(self,
                  model: QuerySet,
                  request: HttpRequest,
                  pk: str,
                  method: str):
        """
        Общий метод удаления и добавления записи в модели
        FavoritesList и ShoppingList.
        """
        answer_text = {
            'favorite': {
                'detail': 'Рецепт успешно удален из избранного.',
                'errors': 'Рецепт уже находится в избранном.',
            },
            'shopping_cart': {
                'detail': 'Рецепт успешно удален из списка покупок.',
                'errors': 'Рецепт уже находится в списке покупок.',
            }
        }
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'DELETE':
            get_object_or_404(
                model,
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(
                {'detail': answer_text[method].get('detail')},
                status=status.HTTP_204_NO_CONTENT
            )
        _, result = model.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if result:
            serializer = CroppedRecipeSerializer(
                recipe,
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        return Response(
            {'errors': answer_text[method].get('errors')},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=('get',),
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Скачать список покупок."""
        ingredients = (
            request.user.customer
            .prefetch_related(
                Prefetch(
                    'recipe__ingredients',
                    queryset=(
                        Ingredient.objects
                        .select_related('name', 'measurement_unit')
                    )
                )
            )
            .values(
                'recipe__ingredients__name',
                'recipe__ingredients__measurement_unit'
            )
            .annotate(total_amount=Sum('recipe__qt_ingredients__amount'))
            .distinct()
        )
        context = {'ingredients': ingredients}
        template = get_template('recipes/recipe.html')
        html = template.render(context)
        pdf_file = (
            weasyprint.HTML(string=html)
            .write_pdf(
                stylesheets=[f'{settings.BASE_DIR}/static/css/main.css']
            )
        )
        response = HttpResponse(
            pdf_file,
            content_type='application/pdf',
            status=status.HTTP_200_OK
        )
        response['Content-Disposition'] = 'filename="shopping_list.pdf"'
        return response
