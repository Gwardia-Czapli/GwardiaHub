from django.shortcuts import render, redirect
from django.utils import timezone

from core.discord_auth import require_user
from core.models import User
from .models import Meeting


# There is link to /panel in navbar, but there is no such view as /panel, so for now it's redirecting
# to /panel/gwardia/meetings
@require_user()
def index(request, _user):
    return redirect("gwardia:meetings")


@require_user()
def meetings(request, user: User):
    upcoming_meetings = Meeting.objects.filter(date__gte=timezone.now()).order_by(
        "-date"
    )
    archival_meetings = Meeting.objects.filter(date__lt=timezone.now()).order_by(
        "-date"
    )
    context = {
        "upcoming_meetings": upcoming_meetings,
        "archival_meetings": archival_meetings,
        user: user.to_json(),
    }
    return render(request, "gwardia/meetings.html", context)
