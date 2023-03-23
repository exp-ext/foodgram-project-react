from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import AuthorSubscription
from .serializers import SetPasswordSerializer, SubscriptionsSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    """
    Пользователи:
    - `GET`: cписок пользователей
    - `POST`: регистрация пользователя
    - `GET`: профиль пользователя по id
    - `GET`/me/: текущий пользователь
    - `POST`/set_password/: изменение пароля
    - `GET`/subscriptions/: мои подписки (в выдачу добавляются рецепты)
    - `POST`/subscribe/: подписаться на пользователя
    - `DELETE`/subscribe/: подписаться на пользователя
    """
    permission_classes = (DjangoModelPermissions,)

    def perform_create(self, serializer: Serializer) -> None:
        """
        Создает нового пользователя и сохраняет его в базе данных.
        """
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=('POST',), detail=False,
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        serializer = SetPasswordSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {'detail': 'Пароль успешно изменен!'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=('GET',), detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request: HttpRequest) -> HttpResponse:
        """
        Мои подписки.
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        """
        queryset = User.objects.filter(subscribers__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=('POST', 'DELETE'), detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request: HttpRequest, id: int) -> HttpResponse:
        """
        Подписаться/отписаться на пользователя:
            Доступно только авторизованным пользователям.
        """
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {'errors': 'Подписки на себя недопустимы.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        publisher = user.subscriptions.filter(author=author)

        if request.method == 'DELETE':
            if publisher.exists():
                publisher.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Вы не подписаны на этого автора.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if publisher.exists():
            return Response(
                {'errors': 'Вы уже подписаны на данного автора.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SubscriptionsSerializer(
                author,
                data=request.data,
                context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        publisher = AuthorSubscription.objects.create(
            user=user,
            author=author
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
