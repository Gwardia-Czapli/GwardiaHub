from django.shortcuts import render
from django.utils import timezone

from .models import NextMeeting


def index(request):
    upcoming_meetings = NextMeeting.objects.filter(date_of_meeting__gte=timezone.now()).order_by("date_of_meeting")
    next_5_meetings = {"next_5_meetings": upcoming_meetings[:5]}
    return render(request, "gwardia/index.html", context=next_5_meetings)
