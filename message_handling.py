BOT_SPEAK = 'bot-speak: '


async def bot_speak(client, message):
    """Function allows mods to control the bot via dm's"""

    speak_data = message.content[len(BOT_SPEAK):].strip()
    speak_channel = speak_data.split(" | ")[0]
    bot_message = speak_data.split(" | ")[1]

    for channel in client.get_all_channels():
        if channel.name == speak_channel:
            await channel.send(bot_message)
            return

    await message.author.send(f"Sorry I could not find the {speak_channel} channel! Please try again!")


async def handle_mentions(client, message):
    """Handles messages that mention the bot"""
    pass