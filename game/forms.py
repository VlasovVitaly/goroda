from django import forms

from .models import Match


class StartNewMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('team1', 'team2')
        widgets = {
            'team1': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'team2': forms.TextInput(
                attrs={'class': 'form-control'}
            )
        }
        labels = {
            'team1': 'First team name',
            'team2': 'Second team name'
        }
