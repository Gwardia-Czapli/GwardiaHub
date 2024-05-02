import requests

from gwardia_hub.settings import CLIENT_ID, CLIENT_SECRET, DEBUG, GUILD_ID

API_ENDPOINT = "https://discord.com/api/v10"
REDIRECT_URI = (
    "http://localhost:8000/auth/discord/code"
    if DEBUG
    else "https://gwardiahub.fly.dev/auth/discord/code"
)
DISCORD_TOKEN_COOKIE = "discord_access_token"
DISCORD_REFRESH_COOKIE = "discord_refresh_token"


class UnauthorizedException(Exception):
    pass


def code_to_token(code):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        f"{API_ENDPOINT}/oauth2/token",
        data=data,
        headers=headers,
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    r.raise_for_status()
    return r.json()


def refresh_token(refresh_token):
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        f"{API_ENDPOINT}/oauth2/token",
        data=data,
        headers=headers,
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    if r.status_code == 401:
        raise UnauthorizedException
    r.raise_for_status()
    return r.json()


def fetch_guild_user(token):
    headers = {
        "Authorization": f"Bearer {token}",
    }
    r = requests.get(
        f"{API_ENDPOINT}/users/@me/guilds/{GUILD_ID}/member",
        headers=headers,
    )
    if r.status_code == 401:
        raise UnauthorizedException
    r.raise_for_status()
    return r.json()
