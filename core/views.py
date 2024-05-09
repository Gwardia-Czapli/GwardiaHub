from django.shortcuts import render
from django.templatetags.static import static


def index(request):
    return render(request, "core/index.html")


def profile(request):
    # Those are placeholder data
    user = {
        "name": "Salieri",
        "roles": ["root", "Gwardyjczyk", "Genshiniara"],
        "level": "42",
        "exp": "621",
        "max_exp": "2137",
    }
    return render(request, "core/profile.html", context={"user": user})


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
