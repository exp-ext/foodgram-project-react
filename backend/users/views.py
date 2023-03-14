from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.serializers import Serializer

User = get_user_model()


class UserViewSet(UserViewSet):
    permission_classes = (DjangoModelPermissions,)

    def perform_create(self, serializer: Serializer) -> None:
        """
        Создает нового пользователя и сохраняет его в базе данных.

        Args:
            self (:obj:`Self@UserSerializer`): Экземпляр класса `UserViewSet`.
            serializer (:obj:`Serializer`): Сериализатор, используемый для
        десериализации данных запроса.

        Return:
            None
        """
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
        user.set_password(serializer.validated_data['password'])
        user.save()
