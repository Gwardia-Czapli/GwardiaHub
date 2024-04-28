from django.shortcuts import render


def index(request):
    return render(request, "core/index.html")


def profile(request):
    # Those are placeholder data
    user = {
        "name": "Salieri",
        "avatar": "https://cdn.discordapp.com/attachments/1022538414328913930/1233483249947381912/texas_pfp_elita.jpg?ex=662f3c8b&is=662deb0b&hm=9b5f3ee44633a27c5b3bcb8a79687f59567f229b5263547ab6565855679d90d5&",
        "roles": ["root", "Gwardyjczyk", "Genshiniara"],
        "level": "42",
        "exp": "621",
        "max_exp": "2137",
    }
    return render(request, "core/profile.html", context={"user": user})
