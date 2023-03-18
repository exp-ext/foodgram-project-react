from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    """
    Фильтр для RecipeViewSet:
    фильтрация по избранному, автору, списку покупок и тегам.
    """
    is_favorited = filters.BooleanFilter(
        method='is_favorited_filter')

    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter')

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(is_favorited__user=user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(is_in_shopping_cart__user=user)
        return queryset
