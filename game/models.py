from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    """City name model."""

    GEOTYPE_CITY = 1,
    GEOTYPE_OTHER = 2,
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
        return '<{}>: {} {}'.format(self.__class__.__name__, self.geotype, self.name)

    def __str__(self):
        return self.name


class Match(models.Model):
    team1 = models.CharField(
        max_length=128,
        default='Team 1'
    )
    team2 = models.CharField(
        max_length=128,
        default='Team 2'
    )
    judge = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='matches', related_query_name='match'
    )
    finished = models.BooleanField(default=False)
    winner = models.PositiveIntegerField(null=True, blank=True)
    current = models.PositiveIntegerField()
    turns_count = models.PositiveIntegerField(default=0)
    started = models.DateTimeField()
    ended = models.DateTimeField(null=True)
    exhaused_letters = models.CharField(max_length=32, blank=True, default='')
    turn_letter = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return 'Game: {} VS {}'.format(self.team1, self.team2)
