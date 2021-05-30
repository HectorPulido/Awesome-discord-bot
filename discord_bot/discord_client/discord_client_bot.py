import discord
import asyncio

from discord import emoji


class BotClient(discord.Client):

    command_stack = []

    def __init__(self, **options):
        loop = asyncio.new_event_loop()
        super().__init__(loop=loop, **options)

    async def on_ready(self):
        while self.command_stack:
            await self.command_stack.pop()()

        await self.close()

    def send_messages(self, messages):
        self.messages = messages
        self.command_stack.append(self._send_messages)

    def get_history(self, limit):
        self.limit = limit
        self.command_stack.append(self._get_history)

    def add_reaction(self, messages_to_react):
        self.messages_to_react = messages_to_react
        self.command_stack.append(self._add_reaction)

    async def _send_messages(self):
        channels_cache = {}
        for message in self.messages:
            if not message["channel"] in channels_cache:
                channels_cache[message["channel"]] = self.get_channel(
                    message["channel"]
                )
            channel = channels_cache[message["channel"]]
            try:
                await channel.send(message["message"])
            except:
                continue

    async def _get_history(self):
        self.message_history = []
        channels = self.get_all_channels()
        for channel in channels:
            try:
                async for message in channel.history(limit=self.limit):
                    self.message_history.append(message)
            except:
                continue

    async def _add_reaction(self):
        channels_cache = {}

        for message, reaction in self.messages_to_react.items():
            channel_id = message.channel.id
            message_id = message.id

            if not channel_id in channels_cache:
                channels_cache[channel_id] = discord.utils.get(
                    self.get_all_channels(), id=channel_id
                )

            channel = channels_cache[channel_id]

            try:
                message = await channel.fetch_message(message_id)
                await message.add_reaction(reaction)
            except:
                continue

    @classmethod
    def get_history_method(cls, key):
        bot = cls()
        bot.get_history(250)
        bot.run(key)
        return bot.message_history

    @classmethod
    def add_reaction_method(cls, key, messages):
        bot = cls()
        bot.add_reaction(messages)
        bot.run(key)

    @classmethod
    def send_messages_method(cls, key, messages):
        bot = cls()
        bot.send_messages(messages)
        bot.run(key)
