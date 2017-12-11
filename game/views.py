from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.db import transaction

from .forms import StartNewMatchForm, TurnForm
from .models import Match


@login_required
def start_page(request):
    context = {}

    return render(request, 'game/start_page.html', context=context)


@login_required
def start_new_match(request):
    context = {}
    context['form'] = start_form = StartNewMatchForm(request.POST or None)

    if start_form.is_valid():
        match = start_form.save(commit=False)
        match.judge = request.user
        match.save()
        return redirect('game:detail', match.id)

    return render(request, 'game/start_new_match.html', context=context)


@login_required
def match_detail(request, match_id):
    context = {}

    context['match'] = match = get_object_or_404(Match, pk=match_id)

    if request.user != match.judge:
        return HttpResponseBadRequest("You are not a judge of this game.")  # TODO Remove or better message

    context['turns'] = match.turns.order_by('num').reverse()
    context['exhaused_letters'] = match.exhaused_letters
    context['turn_form'] = turn_form = TurnForm(match, data=request.POST or None)

    if turn_form.is_valid():
        turn = turn_form.cleaned_data['turn']

        with transaction.atomic():
            turn.save()
            try:
                match.make_turn(turn.city)
            except Match.AllLettersExhaused:
                pass  # TODO End of game.
            match.save()

    return render(request, 'game/match_detail.html', context=context)
