from django.shortcuts import render


def index(request):
    context = {
        "navbar_links": [
            {
                "name": "Panel",
                "url": "panel/",
            },
        ]
    }
    return render(request, "core/index.html", context)


def profile(request, name: str):
    # Those are placeholder data
    user = {
        "name": name,
        "roles": ["root", "Gwardyjczyk", "Genshiniara"],
        "level": "42",
        "exp": "621",
        "max_exp": "2137",
    }
    return render(request, "core/profile.html", context={"user": user})
