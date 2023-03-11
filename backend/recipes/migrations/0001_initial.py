# Generated by Django 4.1.7 on 2023-03-11 09:53

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('title', models.CharField(max_length=256, unique=True, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=16, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
            },
        ),
        migrations.CreateModel(
            name='QuantityIngredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=0, verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Количество',
                'verbose_name_plural': 'Количество',
                'ordering': ('recipe',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('title', models.CharField(max_length=256, unique=True, verbose_name='Название')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='recipe_images/', verbose_name='Картинка')),
                ('text', models.TextField(verbose_name='Текстовое описание')),
                ('cooking_time', models.PositiveSmallIntegerField(default=0, verbose_name='Время приготовления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('title', models.CharField(max_length=256, unique=True, verbose_name='Название')),
                ('color_hex', models.CharField(max_length=7, unique=True, verbose_name='Цветовой HEX-код')),
                ('slug', models.CharField(max_length=64, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
    ]