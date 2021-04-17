from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    value = models.TextField()

    def __str__(self):
        return self.name


class DiscordUser(models.Model):
    nickname = models.CharField(max_length=200)
    discord_id = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.discord_id


class ResourceType(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    channel_id = models.CharField(max_length=10, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    discord_user = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)
    resource_type = models.ForeignKey(
        ResourceType, on_delete=models.CASCADE, db_index=True
    )
    url = models.TextField()
    tags = models.TextField()

    def __str__(self):
        return self.text
