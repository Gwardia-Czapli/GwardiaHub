import functools
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from core.discord_api import (
    DISCORD_REFRESH_COOKIE,
    DISCORD_TOKEN_COOKIE,
    fetch_guild_member,
    DISCORD_ID_COOKIE,
)
from core.models import User, UserRole
from gwardia_hub.settings import MEMBER_ROLE_ID


def require_discord_login(required_role_id: str | None = MEMBER_ROLE_ID):
    """
    Decorator that checks if a user is logged in and has the required role.

    Adds a second positional argument to the decorated function containting the guild member.

    :param required_role_id: A role ID required for the user to be authorised.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request: HttpRequest = args[0]
            token = request.COOKIES.get(DISCORD_TOKEN_COOKIE)
            if token is None:
                return auth_redirect("core:discord_refresh", request)

            discord_id = request.COOKIES.get(DISCORD_ID_COOKIE)
            if discord_id is None:
                user = fetch_guild_member(token)
            else:
                user = User.objects.get(discord_id=discord_id)

            try:
                required_role = UserRole.objects.get(id=required_role_id)
                if not user.roles.contains(required_role):
                    return set_id_cookie(HttpResponse("Unauthorized", status=401), user)
            except UserRole.DoesNotExist:
                pass

            return set_id_cookie(func(*args, user, **kwargs), user)

        return wrapper

    return decorator


def auth_redirect(target: str, request: HttpRequest) -> HttpResponse:
    """
    Does a redirect, but also stores the current url, so we can go back to it later using the go_back function
    """
    request.session["next_url"] = request.build_absolute_uri()
    return redirect(target)


# Redirects to a stored url if set or else to index page
def go_back(request: HttpRequest) -> HttpResponse:
    next_url = request.session.get("next_url")
    if next_url is None:
        return redirect(reverse("core:index"))
    del request.session["next_url"]
    return redirect(next_url)


def set_token_cookies(
    response: HttpResponse, tokens_response: dict[str, str]
) -> HttpResponse:
    response.set_cookie(
        DISCORD_TOKEN_COOKIE,
        tokens_response["access_token"],
        max_age=tokens_response["expires_in"],
    )
    response.set_cookie(
        DISCORD_REFRESH_COOKIE,
        tokens_response["refresh_token"],
        max_age=14 * 24 * 60 * 60,
    )
    return response


def set_id_cookie(response: HttpResponse, user: User) -> HttpResponse:
    response.set_cookie(DISCORD_ID_COOKIE, user.discord_id, max_age=5 * 60)
    return response
