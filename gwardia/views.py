from django.shortcuts import render
from django.utils import timezone

from .models import Meeting


def index(request):
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
    return render(request, "gwardia/index.html", context)
