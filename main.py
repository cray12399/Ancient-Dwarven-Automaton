import os
import re

import discord
from dotenv import load_dotenv

from message_handling import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_GUILD')
CHANNELS = {}

client = discord.Client()


@client.event
async def on_message(message):
    """Handles all incoming messages on the server and passes them to message handler functions"""

    if message.author == client.user:  # If the bot is the message author, ignore it.
        return
    elif type(message.channel) is discord.channel.DMChannel:  # If the message is a dm
        if message.content[:len(BOT_SPEAK)] == BOT_SPEAK:  # If the dm is not a bot-speak command
            await bot_speak(client, message)
    elif client.user.mentioned_in(message):  # If the bot was mentioned
        await handle_mentions(client, message)


@client.event
async def on_member_join(member):
    """Responds to new members joining."""

    await member.create_dm()
    await member.dm_channel.send(
        f'How far ye, {member.name}? Welcome to the cooliest guild on this side of Troelvrth!'
    )


@client.event
async def on_ready():
    """Readies the bot for action! This function must be below every other event function."""

    dnd_server = discord.utils.find(lambda s: s.name == SERVER, client.guilds)
    if dnd_server is not None:
        print(
            f'{client.user} is connected to the following server:\n'
            f'{dnd_server.name}(id: {dnd_server.id})'
        )

    global CHANNELS
    CHANNELS = {c.name: c.id for c in client.get_all_channels()}

    return dnd_server

client.run(TOKEN)


async def main():
    dnd_server = on_ready()


if __name__ == '__main__':
    main()
