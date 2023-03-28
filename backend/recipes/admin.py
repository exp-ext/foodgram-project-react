from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Ingredient, IngredientsInRecipe, Recipe, Tag


class IngredientsInRecipeInline(admin.TabularInline):
    model = IngredientsInRecipe
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientsInRecipeInline,)
    readonly_fields = ('preview',)
    empty_value_display = '-пусто-'
    fieldsets = (
        (None, {'fields': ('name', 'author', 'image', 'preview')}),
        ('Описание', {'fields': ('text',)}),
        ('Другие параметры', {'fields': ('tags', 'cooking_time')}),
    )

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">'
        )


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
    prepopulated_fields = {'slug': ('name',)}
    list_display = (
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
