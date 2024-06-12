from core.discord_auth import user_logged_in

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
    user = user_logged_in(request)
    if user is None:
        return {}
    links = {}
    for role in user.roles.all():
        permission_sidebar = SIDEBAR_LINKS.get(role.permissions)
        if permission_sidebar is None:
            continue
        links[role.permissions] = permission_sidebar
    return {"sidebar_links": links}
