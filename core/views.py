from urllib.parse import urlencode

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.discord_api import (
    CLIENT_ID,
    DISCORD_REFRESH_COOKIE,
    authorise_code,
    refresh_access_token,
    DISCORD_ID_COOKIE,
    fetch_user,
)
from core.discord_auth import (
    go_back,
    require_user,
    set_token_cookies,
    require_no_user,
    set_id_cookie,
    reset_cookies,
)
from core.gh_webhook_handling import handle_webhook
from core.models import User


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


@require_user(required_role_id=None)
def profile(request, user, name: str = None):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        pass
    return render(request, "core/profile.html", context={"user": user.to_json()})


@require_no_user()
def login(request):
    return render(request, "core/login.html")


@require_no_user()
def discord_login(request: HttpRequest):
    query = urlencode(
        {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": request.build_absolute_uri(reverse("core:discord_code")),
            "scope": "identify guilds.members.read",
            "prompt": "none",
        }
    )
    return redirect(f"https://discord.com/oauth2/authorize?{query}")


@require_no_user()
def discord_code(request):
    auth_data = authorise_code(request)
    if auth_data is None:
        return redirect("core:login")
    user = fetch_user(auth_data["access_token"])
    return set_id_cookie(set_token_cookies(go_back(request), auth_data), user)


def discord_refresh(request):
    user_id = request.COOKIES.get(DISCORD_ID_COOKIE)

    if not User.exists(user_id):
        return redirect("core:login")

    token = request.COOKIES.get(DISCORD_REFRESH_COOKIE)
    if token is None:
        return redirect("core:login")
    refresh_token_data = refresh_access_token(token)
    if refresh_token_data is None:
        return redirect("core:login")
    return set_token_cookies(go_back(request), refresh_token_data)


@csrf_exempt
@require_POST
def gh_webhook(request):
    try:
        return HttpResponse(handle_webhook(request))
    except KeyError:
        return HttpResponse("Invalid request", status=500)


@require_user(required_role_id=None)
@require_POST
def logout(request, _user):
    return reset_cookies(redirect("core:index"))


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
