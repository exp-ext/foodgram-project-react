from django.contrib import admin

from .models import Ingredient, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
    )
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
