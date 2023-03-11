from django.core.management.base import BaseCommand, CommandError

from ._convert_from_csv import cvs_to_dj_model


class Command(BaseCommand):
    help = 'Конвертор данных cvs to db.sqlite3'

    def handle(self, *args, **options):
        try:
            cvs_to_dj_model()
        except Exception as error:
            raise CommandError(error)
        self.stdout.write(self.style.SUCCESS(
            'Операция конвертирования завершена успешно'
        ))
