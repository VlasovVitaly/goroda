from collections import defaultdict

from django.core.management.base import BaseCommand

from game.models import City


class Command(BaseCommand):
    help = 'Display all lettest statistics'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        cities_qs = City.objects.filter(geotype=City.GEOTYPE_CITY).only('name')
        city_names = {cty.name for cty in cities_qs}

        letter_counters = defaultdict(lambda: 0)

        for city in city_names:
            letter_counters[city[0].upper()] += 1

        for letter in sorted(letter_counters.keys()):
            self.stdout.write('{}: {}\n'.format(letter, letter_counters[letter]))
