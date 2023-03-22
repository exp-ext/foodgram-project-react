from typing import Any, Dict, List, OrderedDict

from core.serializers import CroppedRecipeSerializer
from core.validators import field_validator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (CharField, ModelSerializer,
                                        ReadOnlyField, Serializer,
                                        SerializerMethodField, ValidationError)

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    Сериализатор для работы с моделью User.
    """
    is_subscribed = SerializerMethodField()
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )

    def validate(self, obj: OrderedDict) -> OrderedDict:
        """
        Валидация тегов и ингридиентов.
        """
        field_list = [
            'email', 'username', 'first_name', 'last_name', 'password'
        ]
        field_validator(obj, field_list)
        return obj

    def get_is_subscribed(self, obj: User) -> bool:
        """
        Возвращает `bool` результат  подписки пользователя на автора.
        """
        user = self.context.get('view').request.user

        if not user.is_authenticated or (user == obj):
            return False

        return user.subscriptions.filter(author=obj).exists()


class SetPasswordSerializer(Serializer):
    """Изменение пароля текущего пользователя."""
    new_password = CharField()
    current_password = CharField()

    class Meta:
        model = User
        fields = (
            'new_password',
            'current_password',
        )
        extra_kwargs = {
            'new_password': {'required': True, 'allow_blank': False},
            'current_password': {'required': True, 'allow_blank': False},
        }

    def validate(self, obj):
        validate_password(obj['new_password'])
        return super().validate(obj)

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise ValidationError(
                {'current_password': 'Неправильный пароль.'}
            )
        if (validated_data['current_password']
                == validated_data['new_password']):
            raise ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего.'}
            )
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data


class SubscriptionsSerializer(Serializer):
    """Сериализатор вывода авторов на которых подписан текущий пользователь.
    """
    email = ReadOnlyField()
    id = ReadOnlyField()
    username = ReadOnlyField()
    first_name = ReadOnlyField()
    last_name = ReadOnlyField()
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj: User) -> bool:
        """
        Проверка подписки пользователей.
        """
        user = self.context['request'].user
        return user.subscriptions.filter(author=obj).exists()

    def get_recipes(self, obj: User) -> List[Dict[str, Any]]:
        """
        Возвращает количество рецептов у автора.
        """
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if limit:
            queryset = queryset[:int(limit)]
        return CroppedRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj: User) -> int:
        """
        Возвращает количество рецептов у автора.
        """
        return obj.recipes.count()
