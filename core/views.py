from django.shortcuts import render


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
