from urllib.parse import urlencode

from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import redirect
from core.discord_api import (
    CLIENT_ID,
    DISCORD_REFRESH_COOKIE,
    authorise_code,
    refresh_access_token,
)
from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.discord_auth import go_back, require_discord_login, set_token_cookies
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


@require_discord_login()
def profile(request, name: str, user):
    # Those are placeholder data
    user = {
        "name": user.username,
        "roles": user.role_names(),
        "level": 42,
        "exp": 621,
        "max_exp": 2137,
        "avatar": user.avatar_url(),
    }
    return render(request, "core/profile.html", context={"user": user})


def login(request):
    return render(request, "core/login.html")


def discord_login(request: HttpRequest):
    query = urlencode(
        {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": request.build_absolute_uri(reverse("core:discord_code")),
            "scope": "identify guilds.members.read",
            "prompt": "confirm",
        }
    )
    return redirect(f"https://discord.com/oauth2/authorize?{query}")


def discord_code(request):
    auth_data = authorise_code(request)
    if auth_data is None:
        return redirect("core:login")

    return set_token_cookies(go_back(request), auth_data)


def discord_refresh(request):
    token = request.COOKIES.get(DISCORD_REFRESH_COOKIE)
    if token is None:
        return redirect("core:login")

    return set_token_cookies(go_back(request), refresh_access_token(token))


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
