from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Meeting


# There is link to /panel in navbar, but there is no such view as /panel, so for now it's redirecting
# to /panel/gwardia/meetings
def index(request):
    return redirect("gwardia:meetings")


def meetings(request):
    upcoming_meetings = Meeting.objects.filter(date__gte=timezone.now()).order_by(
        "-date"
    )
    archival_meetings = Meeting.objects.filter(date__lt=timezone.now()).order_by(
        "-date"
    )
    context = {
        "upcoming_meetings": upcoming_meetings,
        "archival_meetings": archival_meetings,
    }
    return render(request, "gwardia/meetings.html", context)
