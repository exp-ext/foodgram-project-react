# Generated by Django 4.1.7 on 2023-03-22 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_rename_quantityingredients_ingredientsinrecipe_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название'),
        ),
    ]