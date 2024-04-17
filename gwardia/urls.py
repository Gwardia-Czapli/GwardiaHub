from django.urls import path

from . import views

app_name = "gwardia"
urlpatterns = [
    path("", views.index, name="index"),
]
