from datetime import timedelta
from django.utils import timezone
from django.db import models


class UserRole(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField()

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
        default=timezone.now() + timedelta(minutes=10)
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

    @classmethod
    def exists(cls, user_id: int) -> bool:
        try:
            User.objects.get(discord_id=user_id)
        except User.DoesNotExist:
            return False
        return True
