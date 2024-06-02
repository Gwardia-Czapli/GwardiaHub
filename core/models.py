from datetime import datetime
from django.utils import timezone
from django.db import models

ROLE_PERMISSIONS = ["None", "Gwardia", "Genshin", "Klasowe"]


def get_permission_choices():
    return {i: i for i in ROLE_PERMISSIONS}


class UserRole(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField()
    permissions = models.CharField(choices=get_permission_choices, default="")

    def __str__(self):
        return f"{self.name} ({self.id})"


class User(models.Model):
    discord_id = models.BigIntegerField(
        unique=True
    )  # using BigInt as discord IDs are 64-bit ints
    username = models.CharField()
    avatar_hash = models.CharField()
    roles = models.ManyToManyField(UserRole)

    # caching data for 10 minutes to prevent Rate-Limits from Discord API
    data_valid_until = models.DateTimeField(
        default=datetime(1971, 1, 1, tzinfo=timezone.timezone.utc),
    )

    def avatar_url(self):
        return f"https://cdn.discordapp.com/avatars/{self.discord_id}/{self.avatar_hash}.png"

    def __str__(self):
        return f"{self.username}"

    def role_names(self):
        role_names = []
        for role in self.roles.iterator():
            role_names.append(role.name)
        return role_names

    def to_json(self):
        return {
            "name": self.username,
            "roles": self.role_names(),
            "level": 42,
            "exp": 621,
            "max_exp": 2137,
            "avatar": self.avatar_url(),
        }

    def has_permission(self, permission):
        if permission is None:
            return True
        for role in self.roles.all():
            if permission == role.permissions:
                return True

        return False

    @classmethod
    def exists(cls, user_id: int) -> bool:
        try:
            User.objects.get(discord_id=user_id)
        except User.DoesNotExist:
            return False
        return True
