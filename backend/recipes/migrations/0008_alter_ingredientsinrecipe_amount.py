# Generated by Django 4.1.7 on 2023-03-25 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_ingredient_name_alter_recipe_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество'),
        ),
    ]
