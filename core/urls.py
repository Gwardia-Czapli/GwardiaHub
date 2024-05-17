from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("panel/profile/<str:name>", views.profile, name="profile"),
    path("api/gh_webhook", views.gh_webhook, name="gh_webhook"),
]
