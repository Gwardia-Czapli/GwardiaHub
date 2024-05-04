from django.urls import path

from . import views

app_name = "gwardia"
urlpatterns = [
    path("", views.meetings, name="index"),
    path("asdf", views.asdf, name="asdf"),
]
