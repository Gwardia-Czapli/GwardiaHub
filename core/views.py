from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .gh_webhook_handling import handle_webhook


def index(request):
    context = {
        "navbar_links": [
            {
                "name": "Panel",
                "url": "panel/",
            },
        ]
    }
    return render(request, "core/index.html", context)


def profile(request, name: str):
    # Those are placeholder data
    user = {
        "name": name,
        "roles": ["root", "Gwardyjczyk", "Genshiniara"],
        "level": "42",
        "exp": "621",
        "max_exp": "2137",
    }
    return render(request, "core/profile.html", context={"user": user})


@csrf_exempt
@require_POST
def gh_webhook(request):
    try:
        return HttpResponse(handle_webhook(request))
    except KeyError:
        return HttpResponse("Invalid request")
