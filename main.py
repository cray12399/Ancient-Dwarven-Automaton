import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

from message_handling import *
from cogs import GameCommands, UtilityCommands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_GUILD')
CHANNELS = {}

bot = commands.Bot(command_prefix='/', intents=discord.Intents().all())

GAME = None


@bot.event
async def on_message(message):
    """Handles all incoming messages on the server and passes them to message handler functions"""

    if message.author == bot.user:  # If the bot is the message author, ignore it.
        return
    elif type(message.channel) is discord.channel.DMChannel:  # If the message is a dm
        pass
    elif bot.user.mentioned_in(message):  # If the bot was mentioned
        await handle_mentions(bot, message)

    await bot.process_commands(message)


# @bot.event
# async def on_member_join(member):
#     """Responds to new members joining."""
#
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'How fare ye, {member.name}? Welcome to the cooliest guild on this side of Troelvrth!'
#     )


@bot.event
async def on_ready():
    """Readies the bot for action! This function must be below every other event function."""

    dnd_server = discord.utils.find(lambda s: s.name == SERVER, bot.guilds)
    if dnd_server is not None:
        print(
            f'{bot.user} is connected to the following server:\n'
            f'{dnd_server.name}(id: {dnd_server.id})'
        )

    global CHANNELS
    CHANNELS = {c.name: c.id for c in bot.get_all_channels()}

    return dnd_server

bot.add_cog(UtilityCommands(bot))
bot.add_cog(GameCommands(bot))


bot.run(TOKEN)


async def main():
    dnd_server = on_ready()


if __name__ == '__main__':
    main()
