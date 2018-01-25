from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import City


class CityModelTest(TestCase):
    def testUnique(self):
        """All city names must be unique."""
        first = City(name='TEST_NAME')
        first.save()

        second = City(name='TEST_NAME')
        self.assertRaises(ValidationError, second.full_clean)

        first.delete()
