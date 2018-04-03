from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import City


class CityModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_city_name = 'test_city'
        cls.test_city = City.objects.create(name=cls.test_city_name, geotype=City.GEOTYPE_CITY)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_city.delete()

    def testUniqueName(self):
        test_city = City(name=self.test_city_name, geotype=City.GEOTYPE_CITY)
        test_other = City(name=self.test_city_name, geotype=City.GEOTYPE_OTHER)

        self.assertRaises(ValidationError, test_city.full_clean)
        self.assertRaises(ValidationError, test_other.full_clean)
