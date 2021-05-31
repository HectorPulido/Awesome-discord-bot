import re
from django.db import models


class Type(models.Model):
    description = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.description = self.description.lower()
        return super(Type, self).save(*args, **kwargs)


class Channel(models.Model):
    channel_id = models.IntegerField(unique=True, db_index=True)
    guild_name = models.CharField(max_length=255)
    channel_name = models.CharField(max_length=255)
    channel_type = models.ForeignKey(Type, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.channel_name

    @classmethod
    def create_channel(cls, channel, channel_type):
        return cls.objects.create(
            channel_id=channel.id,
            channel_name=channel.name,
            guild_name=channel.guild.name,
            channel_type=channel_type,
        )


class Resource(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, db_index=True)
    message_id = models.IntegerField(db_index=True)
    discord_user = models.IntegerField()
    url = models.CharField(max_length=255)
    description = models.TextField(db_index=True)

    def __str__(self):
        return self.description

    @classmethod
    def create_resource(cls, message, channel):
        resource = cls.objects.filter(message_id=message.id).last()
        if resource:
            return resource

        embeds_url = None
        embeds_description = ""

        for embed in message.embeds:
            if not embeds_url:
                embeds_url = embed.url

            embeds_description += (
                f"| url: {embed.url} + {embed.title} + {embed.description}"
            )

        embeds_description = embeds_description.lower()

        resource, _ = cls.objects.get_or_create(
            channel=channel,
            message_id=message.id,
            discord_user=message.author.id,
            url=embeds_url,
            description=embeds_description,
        )

        return resource
