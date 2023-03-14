from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    Сериализатор для работы с моделью User.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
