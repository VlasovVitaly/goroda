from functools import wraps

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .models import Match


def match_judge_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, match_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_URL)

        match = get_object_or_404(Match, pk=match_id)

        if match.judge_id != request.user.id:
            return HttpResponseBadRequest("Not a judge")  # TODO Remove or better message

        return view_func(request, match, *args, **kwargs)

    return wrapped_view
