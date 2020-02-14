"""
Bot's main frame, here the bot is configured and run.
"""

import os
import discord
from bot_core.ship_matrix import ShipMatrix
from bot_core.chunker import make_chunks


class MyBotClient(discord.Client):
    """
    Extends discord Client functionality.
    """

    def __init__(self):
        super().__init__()
        self.matrix = ShipMatrix()
        self.matrix.get_fetcher().register_to_loop(self.loop)

    async def on_message(self, message):
        """
        Here we define what should happen when a message is received by the bot.

        This function is NOT meant to be used by the user.
        """
        if message.author == self.user:
            return

        if message.content.startswith('!help'):
            msg = 'list of commands:\n\t!hello\n\t!hammerhead\n\t!all ships\n\t!flight ready'
            await message.channel.send(msg)
        elif message.content.startswith('!hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await message.channel.send(msg)
        elif message.content.startswith('!hammerhead'):
            msg = 'rat1on thinks the hammerhead it\'s beautiful'
            await message.channel.send(msg)
        elif message.content.startswith('!all ships'):
            msg = ""
            for ship in self.matrix.get_all():
                msg += "%(name)s:\n\tStatus: %(status)s\n\tlink: <%(link)s>\n" % ship

            for chunk in make_chunks(msg, 2000):
                await message.channel.send(chunk)
        elif message.content.startswith('!flight ready'):
            msg = "Flight Ready ships list:\n\n\n"

            for ship in self.matrix.get_flight_ready():
                msg += "%(name)s:\n\tlink: <%(link)s>\n" % ship

            for chunk in make_chunks(msg, 2000):
                await message.channel.send(chunk)

    async def on_ready(self):
        """
        Here we define what should happen when the bot is ready.

        This function is NOT meant to be used by the user.
        """
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


if __name__ == "__main__":
    with open("token.secret", "r") as secret:
        os.environ['DISCORD_API_TOKEN'] = secret.read()
    client = MyBotClient()
    client.run(os.environ['DISCORD_API_TOKEN'])
