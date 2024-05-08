import requests
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from requests import HTTPError
from requests.exceptions import JSONDecodeError

from core.models import User, UserRole
from gwardia_hub.settings import CLIENT_ID, CLIENT_SECRET, GUILD_ID

API_ENDPOINT = "https://discord.com/api/v10"
DISCORD_TOKEN_COOKIE = "discord_access_token"
DISCORD_REFRESH_COOKIE = "discord_refresh_token"
DISCORD_ID_COOKIE = "discord_id"


def authorise_code(request: WSGIRequest) -> dict[str, str] | None:
    """Returns HTTP JSON response from Discord API or None when authorization fails."""
    code = request.GET.get("code")
    if code is None:
        return None

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": request.build_absolute_uri(reverse("discord_callback")),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        f"{API_ENDPOINT}/oauth2/token",
        data=data,
        headers=headers,
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    try:
        r.raise_for_status()
    except HTTPError:
        return None
    return r.json()


def refresh_access_token(refresh_token):
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        f"{API_ENDPOINT}/oauth2/token",
        data=data,
        headers=headers,
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    if r.status_code == 401:
        return None
    r.raise_for_status()
    return r.json()


def fetch_guild_member(access_token: str) -> User | None:
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(
        f"{API_ENDPOINT}/users/@me/guilds/{GUILD_ID}/member",
        headers=headers,
    )
    if not response.ok:
        return None
    try:
        json = response.json()
    except JSONDecodeError:
        return None

    user = User.objects.get_or_create(discord_id=json["user"]["id"])[0]
    user.username = json["user"]["global_name"] or json["user"]["username"]
    user.avatar_hash = json["user"]["avatar"]
    user.roles.set([])
    for role_id in json["roles"]:
        try:
            role = UserRole.objects.get(id=role_id)
            user.roles.add(role)
        except UserRole.DoesNotExist:
            pass
    user.save()

    return user
