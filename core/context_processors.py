SIDEBAR_LINKS = {
    "Genshin": [
        {"name": "Genshin", "url": "/genshin", "icon": "gamepad"},
    ],
    "Gwardia": [
        {
            "name": "Spotkania",
            "url": "/panel/gwardia/meetings",
            "icon": "calendar-days",
        },
        {"name": "Ankiety", "url": "#", "icon": "square-poll-horizontal"},
        {
            "name": "Prezentacje",
            "url": "https://drive.google.com/drive/folders/13xlbrwUslL-as5f41sypAq84mszobigY?usp=sharing",
            "icon": "file-powerpoint",
            "new_tab": True,
        },
    ],
    "Klasowe": [
        {"name": "Obiady", "url": "#", "icon": "bowl-food"},
        {"name": "Sprawdziany", "url": "#", "icon": "newspaper"},
        {"name": "Zadania", "url": "#", "icon": "paste"},
    ],
}


def sidebar_links(request):
    return {"sidebar_links": SIDEBAR_LINKS}
