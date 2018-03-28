from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import StartNewMatchForm, TurnForm
from .models import Match


@login_required
def start_page(request):
    context = {}

    context['matches'] = request.user.matches.all().order_by('finished', '-ended', '-started')

    return render(request, 'game/start_page.html', context=context)


@login_required
def start_new_match(request):
    context = {}
    context['form'] = start_form = StartNewMatchForm(request.user, request.POST or None)

    if start_form.is_valid():
        match = start_form.save(commit=True)
        return redirect(match)

    return render(request, 'game/start_new_match.html', context=context)


from .decorators import match_judge_required


@match_judge_required
def match_detail(request, match):

    context = {
        'match': match,
        'turns': match.turns.order_by('num').reverse(),
        'exhaused_letters': match.exhaused_letters,
        'turn_form': TurnForm(match, data=request.POST or None),
    }

    form = context['turn_form']
    if form.is_valid():
        turn = form.cleaned_data['turn']

        with transaction.atomic():
            turn.save()
            try:
                match.make_turn(turn.city)
            except Match.AllLettersExhaused:
                pass  # TODO End of game.
            match.save()

    return render(request, 'game/match_detail.html', context=context)


@require_POST
@match_judge_required
def end_match(request, match):
    match.end_match(commit=False)
    match.save()

    if request.is_ajax():
        pass  # FIXME return Json answer

    return redirect(match)
