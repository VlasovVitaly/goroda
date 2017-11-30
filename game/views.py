from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import StartNewMatchForm


@login_required
def start_page(request):
    context = {}

    return render(request, 'game/start_page.html')


@login_required
def start_new_match(request):
    pass
