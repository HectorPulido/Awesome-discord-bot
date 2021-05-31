import re

from django.conf import settings
from discord_client.discord_client_bot import BotClient

from .models import Type, Channel, Resource


class DiscordProcessor:
    def __init__(self) -> None:
        self.command_data = {
            r"^\!save .+": self.save_resource,
            r"^\!add_channel .+": self.add_channel,
            r"^\!search .+": self.search,
            r"^\!remove_channel .+": self.remove_channel,
            r"^\!help": self.help,
        }
        self.key = settings.DISCORD_KEY
        self.messages_to_send = []

    def process_command(self):
        messages_to_react = []
        messages, self.members = BotClient.get_history_method(self.key)

        for message in messages:
            if self.check_reaction(message):
                continue

            for pattern, function in self.command_data.items():
                result = re.match(pattern, message.content)
                if result:
                    messages_to_react.append(message)
                    function(message)
                    continue

        to_add_emoji = dict(zip(messages_to_react, ["👍" for _ in messages_to_react]))

        bot = BotClient()
        bot.add_reaction(to_add_emoji)
        bot.send_messages(self.messages_to_send)
        bot.run(self.key)

    def check_reaction(self, message):
        for reaction in message.reactions:
            if reaction.emoji == "👍":
                return True
        return False

    def save_resource(self, message):
        channel = Channel.objects.filter(channel_id=message.channel.id).last()
        if not channel:
            return

        Resource.create_resource(message, channel)

    def add_channel(self, message):
        if not self.check_is_admin(message):
            message_to_send = {
                "channel": message.channel.id,
                "message": f"No tienes permisos para realizar esta accion, pidele a un administrador que lo haga por ti",
            }
            self.messages_to_send.append(message_to_send)
            return

        channel = Channel.objects.filter(channel_id=message.channel.id).last()
        if channel:
            message_to_send = {
                "channel": message.channel.id,
                "message": f"Este canal ya ha sido agregado con el tipo {channel.channel_type.description}",
            }
            self.messages_to_send.append(message_to_send)
            return

        type = message.content.lower().replace("!add_channel ", "")

        channel_type, _ = Type.objects.get_or_create(description=type)
        channel = Channel.create_channel(message.channel, channel_type)

        message_to_send = {
            "channel": message.channel.id,
            "message": f"Canal agregado correctamente con el tipo {channel.channel_type.description}",
        }

        self.messages_to_send.append(message_to_send)

    def remove_channel(self, message):
        channel = Channel.objects.filter(channel_id=message.channel.id).last()
        if not channel:
            return
        channel.delete()

    def search(self, message):
        channel = Channel.objects.filter(channel_id=message.channel.id).last()
        if not channel:
            return

        message_content = message.content.lower()
        message_content = message_content.replace("!search ", "")
        resource = (
            Resource.objects.filter(description__contains=message_content)
            .order_by("?")
            .first()
        )

        if not resource:
            message_to_send = {
                "channel": message.channel.id,
                "message": f"No he encontrado nada con esos terminos <@{message.author.id}>, por favor intenta con otros terminos",
            }
            self.messages_to_send.append(message_to_send)
            return

        message_to_send = {
            "channel": message.channel.id,
            "message": f"<@{message.author.id}> He encontrado esto, espero te funcione:\n{resource.url}",
        }
        self.messages_to_send.append(message_to_send)

    def help(self, message):
        message_to_send = {
            "channel": message.channel.id,
            "message": "Soy Pequeñin un robot que viene del futuro, pero me pusieron de bibliotecario por alguna razon...",
        }

        self.messages_to_send.append(message_to_send)

    def check_is_admin(self, message):
        member_key = f"{message.author.id}{message.guild.id}"

        if not member_key in self.members:
            return False

        try:
            return self.members[member_key].guild_permissions.administrator
        except:
            return False
