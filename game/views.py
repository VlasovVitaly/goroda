from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .decorators import match_judge_required
from .forms import StartNewMatchForm, TurnForm
from .models import Match


@login_required
def start_page(request):
    context = {
        'matches': request.user.matches.order_by('finished', '-ended', '-started')
    }

    return render(request, 'game/index.html', context=context)


@login_required
def start_new_match(request):
    context = {
        'form': StartNewMatchForm(request.user, request.POST or None)
    }
    start_form = context['form']

    if start_form.is_valid():
        match = start_form.save(commit=True)
        return redirect(match)

    return render(request, 'game/start_new_match.html', context=context)


@match_judge_required
def match_detail(request, match):
    context = {'match': match, 'turns': match.turns.order_by('num').reverse()}

    if match.finished:
        return render(request, 'game/ended_match.html', context=context)

    form = context['turn_form'] = TurnForm(match, data=request.POST or None)

    if form.is_valid():
        turn = form.cleaned_data['turn']

        with transaction.atomic():
            turn.save()
            try:
                match.make_turn(turn.city)
            except Match.AllLettersExhaused:
                match.end()
                pass  # TODO End of game.
            match.save()
        context['turn_form'] = TurnForm(None)

    return render(request, 'game/match_detail.html', context=context)


@match_judge_required
def end_match(request, match):
    match.end()

    return redirect(match)
