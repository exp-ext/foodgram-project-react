from typing import OrderedDict

from rest_framework.serializers import ValidationError


def field_validator(obj: OrderedDict, field_list: list):
    """
    Проверка полей на их присутствие и на пусто.
    """

    for field in field_list:
        check = obj.get(field)
        if not check or check == '':
            raise ValidationError(
                {field: ['Обязательное поле.']}
            )


def ingredients_validator(self):
    """
    Проверка списка ингридиентов на уникальность.
    """
    ingredients = self.initial_data.get('ingredients')
    ingredients_id = tuple(i['id'] for i in ingredients)
    if len(ingredients_id) != len(set(ingredients_id)):
        raise ValidationError(
            {'ingredients': ['Ингредиенты должны быть уникальны.']}
        )
