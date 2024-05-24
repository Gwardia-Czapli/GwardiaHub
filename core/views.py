from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.gh_webhook_handling import handle_webhook


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
        return HttpResponse("Invalid request", status=500)


def handling_403(request, exception):
    context = {
        "error_id": "403",
        "description": "Brak dostępu :( \n Możesz zalogować się na /login",
        "image": static("images/403_image.png"),
    }
    return render(request, "core/error.html", context, status=403)


def handling_404(request, exception):
    context = {
        "error_id": "404",
        "description": "Ojej! Wygląda na to, że jesteś teraz na drodze do nikąd :o",
        "image": static("images/404_image.png"),
    }
    return render(request, "core/error.html", context, status=404)


def handling_500(request):
    context = {
        "error_id": "500",
        "description": "Ojej, coś jest nie tak z naszym serwerem :(",
        "image": static("images/500_image.png"),
    }
    return render(request, "core/error.html", context, status=500)
