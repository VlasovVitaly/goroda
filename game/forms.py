from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Match, Turn, City


class StartNewMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('team1', 'team2')
        widgets = {
            'team1': forms.TextInput(attrs={'class': 'form-control'}),
            'team2': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'team1': _('First team name'),
            'team2': _('Second team name')
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        match = super().save(commit=False)
        match.judge = self.user

        if commit is True:
            match.save()
            self.save_m2m()

        return match


class TurnForm(forms.Form):
    city = forms.CharField(
        max_length=128, required=True, strip=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True})
    )

    def __init__(self, match, *args, **kwargs):
        self.match = match
        super().__init__(*args, **kwargs)

    def clean_city(self):
        city = self.cleaned_data['city']

        # Current letter can be None on first turn
        if self.match.current_letter:
            if self.match.current_letter.lower() != city[0].lower():
                raise ValidationError(_('Turn answer is not begin with current letter'), code='invalid')

        try:
            turn_city = City.objects.get(name__iexact=city, geotype=City.GEOTYPE_CITY)
        except City.DoesNotExist:
            raise ValidationError(
                _('City with name "%(city)s" does not exists'), code='invalid', params={'city': city}
            )
        except City.MultipleObjectsReturned as err:
            raise ValidationError(_('Not ambiguous city name. Please try another'), code='lookup_fail')
            # TODO Serious error. write log / send email

        if self.match.turns.filter(city__iexact=turn_city.name).exists():
            raise ValidationError(_('Already called'), code='invalid')

        return turn_city.name

    def clean(self):
        if 'city' not in self.cleaned_data:
            return self.cleaned_data

        self.cleaned_data['turn'] = Turn(
            match=self.match, city=self.cleaned_data['city'],
            team=self.match.current_team, num=self.match.turns_count
        )

        return self.cleaned_data
