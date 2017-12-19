from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


ALLWAYS_EXHAUSED = 'ЁЪЫЬ'


class City(models.Model):
    """City name model."""

    GEOTYPE_CITY = 1
    GEOTYPE_OTHER = 2

    TYPE_CHOICES = (
        (GEOTYPE_CITY, 'City'),
        (GEOTYPE_OTHER, 'Other place'),
    )

    class Meta:
        default_permissions = ('add', )
        verbose_name = 'City name'
        verbose_name_plural = 'City names'

    name = models.CharField(max_length=128, unique=True, db_index=True)
    geotype = models.PositiveIntegerField(choices=TYPE_CHOICES, default=GEOTYPE_CITY)

    def __repr__(self):
        return '<{}>:[{}] {}'.format(self.__class__.__name__, self.geotype, self.name)

    def __str__(self):
        return self.name


class Match(models.Model):
    team1 = models.CharField(max_length=128, default='Team 1')
    team2 = models.CharField(max_length=128, default='Team 2')
    judge = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='matches', related_query_name='match'
    )
    current_team = models.PositiveIntegerField(default=1)
    current_letter = models.CharField(max_length=1, null=True, default=None)
    finished = models.BooleanField(default=False)
    winner = models.PositiveIntegerField(null=True, blank=True)
    turns_count = models.PositiveIntegerField(default=0)
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True)
    exhaused_letters = models.CharField(max_length=32, blank=True, default=ALLWAYS_EXHAUSED)
    turn_letter = models.CharField(max_length=1, blank=True)

    class AllLettersExhaused(Exception):
        pass

    @property
    def current_team_name(self):
        return self.team1 if self.current_team == 1 else self.team2

    @property
    def next_team(self):
        return 1 if self.current_team != 1 else 2

    def make_turn(self, turn_word, commit=False):
        self.current_team = self.next_team
        self.turns_count += 1

        turn_word = turn_word.upper()
        turn_letter = turn_word[0]

        casted_cities = self.turns.filter(city__istartswith=turn_letter).values_list('city', flat=True)

        available = City.objects.filter(name__istartswith=turn_letter, geotype=City.GEOTYPE_CITY)
        available = available.exclude(name__in=casted_cities)

        if not available.exists():
            self.exhaused_letters += turn_letter

        for letter in reversed(turn_word):
            if letter not in self.exhaused_letters:
                self.current_letter = letter
                break
        else:
            # FIXME Exception text can be improved
            raise self.AllLettersExhaused()

        if commit is True:
            self.save()

    def end_match(self, commit=False):
        self.finished = True
        self.ended = timezone.now()
        self.winner = self.next_team

        if commit is True:
            self.save()

    def __repr__(self):
        return '<{}>: {} [{}, {}]'.format(self.__class__.__name__, self.id, self.team1, self.team2)

    def __str__(self):
        return 'Match: {} VS {}'.format(self.team1, self.team2)


class Turn(models.Model):
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE,
        related_name='turns', related_query_name='+'
    )
    city = models.CharField(max_length=128)
    team = models.PositiveSmallIntegerField()
    num = models.PositiveIntegerField()

    def __repr__(self):
        return '<{}>: {}/{} -> {}'.format(self.__class__.__name__, self.match_id, self.num, self.city)

    def __str__(self):
        return 'Turn #{}: Team "{}" vs "{}"'.format(self.num, self.team, self.city)
