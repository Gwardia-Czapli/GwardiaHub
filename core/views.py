from urllib.parse import urlencode
from django.shortcuts import redirect
from core.discord_api import (
    CLIENT_ID,
    DISCORD_REFRESH_COOKIE,
    REDIRECT_URI,
    code_to_token,
    refresh_token,
)
from core.discord_auth import go_back, require_discord_login, set_cookies
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


@require_discord_login()
def profile(request, name: str, _):
    # Those are placeholder data
    user = {
        "name": name,
        "roles": ["root", "Gwardyjczyk", "Genshiniara"],
        "level": "42",
        "exp": "621",
        "max_exp": "2137",
    }
    return render(request, "core/profile.html", context={"user": user})


def login(request):
    return render(request, "core/login.html")


def discord_login(_):
    query = urlencode(
        {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "scope": "identify guilds.members.read",
            "prompt": "none",
        }
    )
    return redirect(f"https://discord.com/oauth2/authorize?{query}")


def discord_code(request):
    code = request.GET["code"]
    auth_data = code_to_token(code)
    return set_cookies(go_back(request), auth_data)


def discord_refresh(request):
    token = request.COOKIES.get(DISCORD_REFRESH_COOKIE)
    if token is None:
        return redirect("core:login")

    return set_cookies(go_back(request), refresh_token(token))


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
