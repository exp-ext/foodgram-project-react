from recipes.models import Recipe
from rest_framework.serializers import ModelSerializer


class CroppedRecipeSerializer(ModelSerializer):
    """Сериализатор для вывода определённого набора полей."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
