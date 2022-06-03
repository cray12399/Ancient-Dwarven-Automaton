# TODO Add commands to cog in this file
# https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
import random

from discord.ext import commands

from game import Game
from views import ConfirmView
import utils


class UtilityCommands(commands.Cog):
    """Commands that are used as general server utility commands rather than DnD game commands."""

    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "Utility Commands"

    @commands.command(
        name="bot-speak",
        aliases=['bs'],
        help="Makes the bot send a custom message to the server.\nFormat: /bot-speak {channel name} \"{message}\"",
        brief="Makes the bot send a custom message to the server."
    )
    async def b_speak(self, ctx, channel, message):
        for c in self.bot.get_all_channels():
            if c.name == channel:
                await c.send(message)
                return

        await ctx.reply(f"Channel: \"{channel}\" not found! Unable to send message!")


class GameCommands(commands.Cog):
    """Commands used to control the flow of the DnD game."""

    def __init__(self, bot):
        self.bot = bot
        self.game = None

        self.__cog_name__ = "Game Commands"

    @commands.command(
        name="/dungeon-master",
        aliases=['dm'],
        help="Assigns a new dungeon master. Dungeon master must be @mentioned in the assignment.",
        brief="Assigns a new dungeon master."
    )
    async def dungeon_master_command(self, ctx, dungeon_master):
        if "Direct Message" in str(ctx.channel):
            await ctx.reply("**ERROR:** This command cannot be called via direct message!")
            return
        elif self.game is None:
            await ctx.reply("**ERROR:** Cannot assign a new Dungeon Master as there is not a game running!")
            return
        elif str(ctx.author.id) != self.game.get_dm():
            await ctx.reply(f"**ERROR:** Only the Dungeon Master:"
                            f" <@{self.game.get_dm()}> can assign a new Dungeon Master!")
            return
        else:
            dm_id = await utils.find_user_id(ctx, dungeon_master.replace('<@', '').replace('>', ''))

            # check if the specified Dungeon Master actually exists in the server.
            if dm_id is not None:  # If someone that goes by that id exists, assign them as the new DM.
                self.game.set_dm(dm_id)
                await ctx.reply(f"<@{self.game.get_dm()}> is the new Dungeon Master!")
            else:  # If not, keep the DM the same.
                await ctx.reply(f"**ERROR:** Specified Dungeon Master: {dungeon_master} not found. No changes made.")

    @commands.command(
        name="/new-game",
        aliases=['ng'],
        help="Creates a new game. Whoever calls the command will "
             "automatically be set as Dungeon Master unless specified",
        brief="Creates a new game."
    )
    async def new_game(self, ctx, dungeon_master=None):
        if "Direct Message" in str(ctx.channel):
            await ctx.reply("**ERROR:** This command cannot be called via direct message!")
            return

        async def override_game():
            """Overrides the game or creates a new one if one does not exist."""

            dm = str(ctx.author.id)

            if dungeon_master is not None:  # If a dungeon master is specified, check if they exist and assign them.
                dm_id = await utils.find_user_id(ctx, dungeon_master.replace('<@', '').replace('>', ''))
                dm = str(ctx.author.id) if dm_id is None else dm_id

            # If a dungeon master is specified, but they could not be found, default to the user who called the command.
            if dungeon_master is not None and dm == str(ctx.author.id):
                await ctx.reply(f"**ERROR:** Specified Dungeon Master: {dungeon_master} not found. "
                                f"Defaulting to <@{dm}>. "
                                f"You can change this with the /dungeon-master command.")

            self.game = Game(dm)
            await ctx.channel.send(f"Huzzah! A new game has begun! <@{dm}> is the Dungeon Master! ")

        async def dont_override():
            await ctx.channel.send("Game override canceled!")

        if self.game is None:
            await override_game()
        else:
            await ctx.reply("A game is already in progress! Do you wish to override it?",
                            view=ConfirmView(yes_function=override_game,
                                             no_function=dont_override))

    @commands.command(
        name="roll-dice",
        aliases=['rd'],
        help="Makes the bot roll dice.",
        brief="Makes the bot roll dice."
    )
    async def roll_dice(self, ctx, rolls, dice_type, modifier=None):
        if "Direct Message" in str(ctx.channel):
            await ctx.reply("**ERROR:** This command cannot be called via direct message!")
            return

        roll_values = []

        # ----- Error checking ----- #
        if not utils.check_int(rolls):
            await ctx.reply(f"**ERROR:** Number of rolls must be an integer.")
            return
        elif not utils.check_int(dice_type.replace('d', '')):
            await ctx.reply(f"**ERROR:** Dice type must be an integer.")
            return
        elif modifier is not None:
            if not utils.check_int(modifier):
                await ctx.reply(f"**ERROR:** Modifier must be an integer.")
                return

        roll_range = int(dice_type.replace('d', ''))
        if roll_range <= 2:
            await ctx.reply(f"**ERROR:** {dice_type} is an invalid dice type!")
            return

        rolls = int(rolls)
        if rolls <= 0:
            await ctx.reply(f"**ERROR:** {rolls} is an invalid value for number of rolls. "
                            f"Must be greater than or equal to 1.")
            return
        # -------------------------- #

        modifier = int(modifier) if modifier is not None else 0  # If there is no modifier, just assume 0.
        for _ in range(int(rolls)):
            roll_values.append(random.randint(1, roll_range) + modifier)  # Appends result of roll + any modifier.

        roll_results = f"**Roll Results:** {roll_values}\n"

        if rolls > 1:
            roll_results += f"**Sum:** {sum(roll_values)}\n**Advantage:** {max(roll_values)}\n"

        await ctx.reply(roll_results)

    @commands.command(
        name="/load-character",
        aliases=['lc'],
        help="Loads your character attributes from DnD Beyond so the bot can track them.",
        brief="Loads your character attributes from DnD Beyond"
                 )
    async def load_character(self, ctx, dnd_beyond_url):
        utils.load_character(ctx.author, dnd_beyond_url)
