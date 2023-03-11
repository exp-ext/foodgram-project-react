from django.db import models


class CreationDate(models.Model):
    """Абстрактная модель для даты создания."""
    creation_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        db_index=True
    )
    class Meta:
        ordering = ('-creation_date',)
        abstract = True


class CommonFieldsModel(CreationDate):
    """Абстрактная модель для повторяющихся полей."""    
    title = models.CharField(
        verbose_name='Название',
        max_length=256,
        unique=True,
    )

    class Meta:
        ordering = ('title',)
        abstract = True
