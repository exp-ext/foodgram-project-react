from django.db import models
from django.utils.translation import gettext_lazy as _


class CreationDate(models.Model):
    """Абстрактная модель для даты создания."""
    creation_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-creation_date',)
        abstract = True


class CommonFieldsModel(CreationDate):
    """Абстрактная модель для повторяющихся полей."""
    name = models.CharField(
        verbose_name=_('Название'),
        null=False,
        blank=True,
        max_length=200,
    )

    class Meta:
        ordering = ('name',)
        abstract = True
