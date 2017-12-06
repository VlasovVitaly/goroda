from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

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
    context['exhaused_letters'] = match.exhaused_letters  # TODO add allways exhaused letters here
    context['turn_form'] = TurnForm()

    return render(request, 'game/match_detail.html', context=context)
