from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, Tag
from rest_framework.serializers import ModelSerializer, SerializerMethodField
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
        fields = '__all__'
        read_only_fields = '__all__',


class RecipeSerializer(ModelSerializer):
    """
    Сериализатор рецептов.
    """
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = '__all__',
