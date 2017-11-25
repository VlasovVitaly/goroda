from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from game.models import City


class Command(BaseCommand):
    help = 'Import city names from file'

    def add_arguments(self, parser):
        parser.add_argument('filename', help='input file name')

    def handle(self, *args, **options):
        fname = options['filename']

        try:
            with open(fname, 'r') as cfile:
                city_names = {line.strip() for line in cfile}
        except IOError as err:
            raise CommandError('Error while file reading. {}'.format(err))

        try:
            with transaction.atomic():
                City.objects.all().delete()

                for city in sorted(city_names):
                    City.objects.create(name=city, geotype=City.GEOTYPE_CITY)
        except BaseException as err:
            raise CommandError('{}'.format(err))

        self.stdout.write('Import successfully finished.')
