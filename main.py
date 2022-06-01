import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

from message_handling import *
from game import Game
from views import ConfirmView

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_GUILD')
CHANNELS = {}

bot = commands.Bot(command_prefix='/')

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


@bot.event
async def on_member_join(member):
    """Responds to new members joining."""

    await member.create_dm()
    await member.dm_channel.send(
        f'How far ye, {member.name}? Welcome to the cooliest guild on this side of Troelvrth!'
    )


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


@bot.command(
    name="bot-speak",
    aliases=['bs'],
    help="Makes the bot send a custom message to the server.\nFormat: /bot-speak {channel name} \"{message}\""
             )
async def bot_speak(ctx, channel, message):
    for c in bot.get_all_channels():
        if c.name == channel:
            await c.send(message)
            return

    await ctx.reply(f"Channel: \"{channel}\" not found! Unable to send message!")


@bot.command(
    name="roll-dice",
    aliases=['rd'],
    help="Makes the bot roll dice.\n Format: /roll-dice {number of rolls} {dice type} {OPTIONAL: modifier}"
             )
async def roll_dice(ctx, rolls, dice_type, modifier=0):
    roll_values = []

    try:
        roll_range = int(dice_type.replace('d', ''))
        try:
            rolls = int(rolls)
            try:
                modifier = int(modifier)
                for _ in range(int(rolls)):
                    roll_values.append(random.randint(1, roll_range + 1) + modifier)
                await ctx.reply(f"Roll Results: {roll_values}\n"
                                f"Sum: {sum(roll_values)}\n"
                                f"Advantage: {max(roll_values)}\n")

            except TypeError:
                await ctx.reply("Could not roll! Modifier is not an integer!")
        except TypeError:
            await ctx.reply("Could not roll! Number of rolls is not an integer!")
    except ValueError:
        await ctx.reply("Could not roll! Dice type unrecognized!")


@bot.command(
    name="/new-game",
    aliases=['ng'],
    help="Creates a new game. Whoever calls the command will automatically be set as dungeon master."
             )
async def new_game(ctx):
    global GAME

    async def override_game():
        global GAME
        GAME = Game(ctx.author)
        await ctx.channel.send("Huzzah! A new game has begun!")

    async def dont_override():
        await ctx.channel.send("Game override canceled!")

    if GAME is None:
        await override_game()
    else:
        await ctx.reply("A game is already in progress! Do you wish to override it?",
                        view=ConfirmView(yes_function=override_game,
                                         no_function=dont_override))


bot.run(TOKEN)


async def main():
    dnd_server = on_ready()


if __name__ == '__main__':
    main()
