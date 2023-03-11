import csv

from django.conf import settings
from recipes.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

PROJECT_DIR = settings.BASE_DIR

MODEL_DICT = {
    User: 'user.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'title.csv',
    GenreTitle: 'genretitle.csv',
    Review: 'review.csv',
    Comment: 'comment.csv',
}


def cvs_to_dj_model():
    """Функция конвертора данных cvs to db.sqlite3 средствами Django"""
    for model, cvs_file in MODEL_DICT.items():
        file = f'{PROJECT_DIR}/static/data/{cvs_file}'
        with open(file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            objs = tuple(model(**data) for data in reader)
            model.objects.bulk_create(objs)
