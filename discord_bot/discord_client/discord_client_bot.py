import discord
import hashlib


class BotClient(discord.Client):
    async def get_history(self, channel_id, limit_data, callback):
        message_history = []
        channel = self.get_channel(channel_id)

        async for msg in channel.history(
            limit=100
        ):  # As an example, I've set the limit to 10000
            if len(msg.embeds) != 0:
                for embed in msg.embeds:
                    aux_message = {
                        "hash": hashlib.md5(embed.url),
                        "title": embed.title,
                        "description": embed.description,
                        "link": embed.url,
                        "user": msg.author.id,
                        "user": msg.author.name,
                    }

                    message_history.append(aux_message)
        callback(message_history)

    async def on_ready(self) -> None:
        for command, keywords in self.command_list.items():
            await self.commands_dict[command](*(keywords))
        await self.close()

    def set_commands(self, command_list):
        self.command_list = command_list
        self.commands_dict = {"get_history": self.get_history}
