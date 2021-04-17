from django.conf import settings
from resources.models import Resource, DiscordUser, ResourceType
from discord_client.discord_client_bot import BotClient


message_history_data = []


def history_callback(channel):
    def history_chanel_callback(message_history):
        for message in message_history:
            message_history_data.append(message)

    return history_chanel_callback


def run():
    bot = BotClient()

    command_list = {"get_history": (508947176337047562, 10, history_callback)}

    bot.set_commands(command_list)
    bot.run(settings.DISCORD_KEY)

    for message in message_history_data:
        discord_user, _ = DiscordUser.objects.get_or_create(
            discord_id=message["user"], nickname=""
        )
        Resource.objects.create(
            discord_user=discord_user, resource_type=None, text=message["description"]
        )
