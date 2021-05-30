from django.conf import settings
from resources.models import Resource
from discord_client.discord_client_bot import BotClient


def run():
    bot = BotClient()
    bot.get_history(100)
    bot.run(settings.DISCORD_KEY)

    to_add_emoji = dict(
        zip(bot.message_history, ["\N{THUMBS UP SIGN}" for i in bot.message_history])
    )

    bot = BotClient()
    bot.add_reaction(to_add_emoji)
    bot.run(settings.DISCORD_KEY)
