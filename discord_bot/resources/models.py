from django.db import models

class Type(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description



class Channel(models.Model):
    channel_id = models.IntegerField()
    guild_name = models.CharField(max_length=255)
    channel_name = models.CharField(max_length=255)
    channel_type = models.ForeignKey(
        Type, on_delete=models.CASCADE, db_index=True
    )

    def __str__(self):
        return self.channel_name


class Resource(models.Model):
    channel_id = models.IntegerField()
    discord_id = models.IntegerField()
    discord_user = models.IntegerField()
    url = models.CharField(max_length=255)
    description = models.TextField()
    resource_type = models.ForeignKey(
        Type, on_delete=models.CASCADE, db_index=True
    )

    def __str__(self):
        return self.description
