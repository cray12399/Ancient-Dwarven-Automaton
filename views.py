import discord


class ConfirmView(discord.ui.View):
    """A confirmation view that contains simple yes and no buttons."""

    def __init__(self, yes_function=None, no_function=None):
        super().__init__()
        self.__yes = yes_function
        self.__no = no_function

    @discord.ui.button(label="Yes", row=0, style=discord.ButtonStyle.danger, emoji="👍")
    async def yes_button_callback(self, button, interaction):
        if self.__yes is not None:
            await self.__yes()
        await self.__disable_buttons(interaction)

    @discord.ui.button(label="No", row=0, style=discord.ButtonStyle.primary, emoji="👎")
    async def no_button_callback(self, button, interaction):
        if self.__no is not None:
            await self.__no()
        await self.__disable_buttons(interaction)

    async def __disable_buttons(self, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
