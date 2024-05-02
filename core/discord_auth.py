import functools
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from core.discord_api import (
    DISCORD_REFRESH_COOKIE,
    DISCORD_TOKEN_COOKIE,
    UnauthorizedException,
    fetch_guild_user,
)
from gwardia_hub.settings import MEMBER_ROLE_ID


# Usage
# Add @require_discord_login() to a view to require the user to be logged in via discord
# This adds a second positional argument containing the guild member object from discord api
# https://discord.com/developers/docs/resources/guild#guild-member-object
# Example
# @require_discord_login()
# def index(request, user):
# By defult the user needs the member role to pass, but optionally you can pass a role id to override this behaviour
# E.g. @require_discord_login("123456789") will require the user to have a role with id 123456789
# Note: Python's way of defining decorators is far from being sane
def require_discord_login(required_role=MEMBER_ROLE_ID):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request: HttpRequest = args[0]
            token = request.COOKIES.get(DISCORD_TOKEN_COOKIE)
            if token is None:
                return bounce_redirect("core:discord_refresh", request)

            try:
                discord_user = fetch_guild_user(token)
            except UnauthorizedException:
                return bounce_redirect("core:discord_refresh", request)

            if required_role not in discord_user["roles"]:
                return HttpResponse("Unauthorized", status=401)

            return func(*args, discord_user, **kwargs)

        return wrapper

    return decorator


# Does a redirect, but also stores the current url, so we can go back to it later using the go_back function
def bounce_redirect(target, request):
    request.session["next_url"] = request.build_absolute_uri()
    return redirect(target)


# Redirects to a stored url if set or else to index page
def go_back(request: HttpRequest):
    next_url = request.session.get("next_url")
    if next_url is None:
        return redirect(reverse("core:index"))
    del request.session["next_url"]
    return redirect(next_url)


def set_cookies(response: HttpResponse, tokens_response):
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
