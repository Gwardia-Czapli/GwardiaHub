from django.urls import include, path

from . import views

login_urls = [
    path("discord/login", views.discord_login, name="discord_login"),
    path("discord/code", views.discord_code, name="discord_code"),
    path("discord/refresh", views.discord_refresh, name="discord_refresh"),
    path("logout", views.logout, name="logout"),
]

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("panel/profile/", views.profile, name="profile"),
    path("auth/", include(login_urls)),
    path("panel/profile/<str:name>", views.profile, name="profile"),
    path("api/gh_webhook", views.gh_webhook, name="gh_webhook"),
    path("login", views.login, name="login"),
]
