import functools
import typing

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from core.discord_api import (
    DISCORD_REFRESH_COOKIE,
    DISCORD_TOKEN_COOKIE,
    fetch_user,
    DISCORD_ID_COOKIE,
)
from core.models import User, UserRole


def user_logged_in(request: HttpRequest) -> User | None:
    """Returns user if logged in."""
    token = request.COOKIES.get(DISCORD_TOKEN_COOKIE)
    if token is None:
        return None

    discord_id = int(request.COOKIES.get(DISCORD_ID_COOKIE))
    fetched_user = fetch_user(token)
    if discord_id is None:
        return fetched_user
    elif fetched_user.discord_id != discord_id:
        print(fetched_user.discord_id, discord_id)
        return None
    return User.objects.get(discord_id=discord_id)


def require_no_user():
    def decorator(func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            if user_logged_in(request):
                return redirect("core:profile")
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_user(required_permissions: str = None):
    """Decorator that checks if a user is logged in and has the required role.

    Adds a second positional argument to the decorated function containting the guild member.

    :param required_permissions: The required permissions.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            user = user_logged_in(request)
            if not user:
                return temporary_redirect("core:discord_refresh", request)
            try:
                if not user.has_permission(required_permissions):
                    return redirect("core:profile", request)
            except UserRole.DoesNotExist:
                pass

            return set_id_cookie(func(request, *args, user, **kwargs), user)

        return wrapper

    return decorator


def temporary_redirect(target: str, request: HttpRequest) -> HttpResponse:
    """Does a temporary redirect that can be reverted using `go_back` method."""
    request.session["next_url"] = request.build_absolute_uri()
    return redirect(target)


def go_back(request: HttpRequest) -> HttpResponse:
    """Redirects to a stored url if set or else to index page"""
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


def reset_cookies(response: HttpResponse) -> HttpResponse:
    response.delete_cookie(DISCORD_ID_COOKIE)
    response.delete_cookie(DISCORD_TOKEN_COOKIE)
    response.delete_cookie(DISCORD_REFRESH_COOKIE)
    return response
