from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import StartNewMatchForm


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
        # TODO redirect to match details

    return render(request, 'game/start_new_match.html', context=context)
