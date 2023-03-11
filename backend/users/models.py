from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from core.models import CreationDate


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Администратор')
        USER = 'user', _('Авторизованный пользователь')

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=256,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )
    is_blocked = models.BooleanField(
        verbose_name='Состояние прав пользователя',
        default=False
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_superuser
            or self.is_staff
        )


class Author_Subscription(CreationDate):
    author = models.ForeignKey(
        verbose_name='Автор',
        related_name='subscribers',
        to=User,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Подписчик',
        related_name='subscriptions',
        to=User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'user'),
                name='\nRepeat subscription\n',
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='\nNo self subscription\n'
            )
        )

    def __str__(self) -> str:
        return f'{self.user.username} -> {self.author.username}'
