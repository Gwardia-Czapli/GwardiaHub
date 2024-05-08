from django.db import models


class UserRole(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField()


class User(models.Model):
    discord_id = models.BigIntegerField(
        unique=True
    )  # using BigInt as discord IDs are 64-bit ints
    username = models.CharField()
    avatar_hash = models.CharField()
    roles = models.ManyToManyField(UserRole)

    def avatar_url(self):
        return f"https://cdn.discordapp.com/avatars/{self.discord_id}/{self.avatar_hash}.png"

    def __str__(self):
        return f"{self.username}"

    def role_names(self):
        role_names = []
        for role in self.roles.iterator():
            role_names.append(role.name)
        return role_names
