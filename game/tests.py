from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from .models import City, Match


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


class MatchModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_username = 'judge'
        cls.test_user = User.objects.create_user(cls.test_username)

        cls.test_team_name = 'blabflipblob'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        cls.test_user.delete()

    def test_next_team_prop(self):
        match = Match(judge=self.test_user)

        match.current_team = 1
        self.assertEqual(match.next_team, 2)

        match.current_team = 2
        self.assertEqual(match.next_team, 1)

    def test_current_team_name_property(self):
        match = Match(judge=self.test_user, current_team=1, team1=self.test_team_name, team2='nope')

        self.assertEqual(self.test_team_name, match.current_team_name)

    def test_end_game(self):
        match = Match.objects.create(
            judge=self.test_user, current_team=1, finished=False, winner=None, ended=None
        )

        match.end()
        match.refresh_from_db()
        match.delete()

        self.assertTrue(match.finished)
        self.assertEqual(match.winner, 2)
        self.assertIsNotNone(match.ended)


    def test_winner_name_property(self):
        test_winner_name = 'blabflipbob'
        match = Match.objects.create(
            judge=self.test_user, current_team=1, team1='nope', team2=self.test_team_name
        )

        match.end()
        match.refresh_from_db()
        match.delete()

        self.assertEqual(self.test_team_name, match.winner_name)
