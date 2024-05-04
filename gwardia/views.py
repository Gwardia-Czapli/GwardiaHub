from django.shortcuts import render
from django.utils import timezone

from .models import Meeting

SIDEBAR_LINKS = {
    "Gwardia": [
        {"name": "Spotkania", "url": "/gwardia", "icon": "calendar-days"},
        {"name": "Ankiety", "url": "#", "icon": "square-poll-horizontal"},
        {
            "name": "Prezentacje",
            "url": "https://drive.google.com/drive/folders/13xlbrwUslL-as5f41sypAq84mszobigY?usp=sharing",
            "icon": "file-powerpoint",
            "new_tab": True,
        },
    ],
    "Klasowe": [
        {"name": "Obiady", "url": "#", "icon": "bowl-food"},
        {"name": "Sprawdziany", "url": "#", "icon": "newspaper"},
        {"name": "Zadania", "url": "#", "icon": "paste"},
    ],
}


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
        "sidebar_links": SIDEBAR_LINKS,
    }
    return render(request, "gwardia/index.html", context)
