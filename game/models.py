from django.db import models


class City(models.Model):
    """City name model."""

    TYPE_CHOICES = (
        (1, 'City'),
        (2, 'Other place'),
    )

    class Meta:
        default_permissions = ('add', )
        verbose_name = 'City name'
        verbose_name_plural = 'City names'

    name = models.CharField(max_length=128, unique=True, db_index=True)
    geotype = models.PositiveIntegerField(choices=TYPE_CHOICES)

    def __repr__(self):
        return '<{}>: {} {}'.format(self.__class__.__name__, self.geotype, self.name)

    def __str__(self):
        return self.name
