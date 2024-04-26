from django.shortcuts import render


def index(request):
    return render(request, "core/index.html")


def profile(request):
    # Those are placeholder data
    user = {
        "name": "Salieri",
        "avatar": "https://media.discordapp.net/attachments/1022538414328913930/1233483249947381912/texas_pfp_elita.jpg?ex=662d424b&is=662bf0cb&hm=09d607554ab28f1bc14c958b2210a0551bd83552077129848e167c7637e18c1b&=&format=webp&width=475&height=475",
        "roles": ["root", "Gwardyjczyk", "Genshiniara"],
        "level": "42",
        "exp": "621",
    }
    return render(request, "core/profile.html", context={"user": user})
