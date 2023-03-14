from rest_framework.filters import SearchFilter


class IngredientSearchFilter(SearchFilter):
    """Поиск ингредиентов по имени."""

    search_param = 'name'
