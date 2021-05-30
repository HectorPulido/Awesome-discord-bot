import re

from django.conf import settings
from discord_client.discord_client_bot import BotClient


from .models import Type, Channel, Resource


class DiscordProcessor:
    def __init__(self) -> None:
        self.command_data = {
            r"^\!save .+": self.save_resource,
            r"^\!addchannel .+": self.add_channel,
            r"^\!remove_channel .+": self.remove_channel,
            r"^\!help": self.help,
        }
        self.key = settings.DISCORD_KEY
        self.messages_to_send = []

    def process_command(self):
        messages_to_react = []
        messages = BotClient.get_history_method(self.key)

        for message in messages:
            for pattern, function in self.command_data.items():
                #TODO ALREADY EXECUTED FUNCTIONS
                result = re.match(pattern, message.content)
                if result:
                    messages_to_react.append(message)
                    function(message)

        BotClient.send_messages_method(self.key, self.messages_to_send)

        to_add_emoji = dict(zip(messages_to_react, ["\N{THUMBS UP SIGN}" for _ in messages_to_react]))

        BotClient.add_reaction_method(self.key, to_add_emoji)

    def save_resource(self, message):
        channel = Channel.objects.filter(channel_id=message.channel.id).last()
        if not channel:
            # return
            channel_type = Type.objects.last()
            channel = Channel.create_channel(message.channel, channel_type)

        Resource.create_resource(message, channel)

    def add_channel(self, message):
        channel = Channel.objects.filter(channel_id=message.channel.id).last()
        if channel:
            return

        channel_type = Type.objects.last()
        Channel.create_channel(message.channel, channel_type)

    def remove_channel(self, message):
        channel = Channel.objects.filter(channel_id=message.channel.id).last()
        if not channel:
            return
        channel.delete()

    def help(self, message):
        message_to_send = {
            "channel": message.channel.id, 
            "message": "Soy Pequeñin un robot que viene del futuro, pero me pusieron de bibliotecario"
        }

        self.messages_to_send.append(message_to_send)
