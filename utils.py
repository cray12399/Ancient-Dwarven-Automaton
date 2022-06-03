# TODO Need to install selenium and use selenium to get DnD Beyond Data.
import pickle


def load_character(user, character_url):
    pass


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


async def find_user_id(ctx, user_id):
    async for member in ctx.guild.fetch_members(limit=None):
        if str(user_id) == str(member.id):
            return str(user_id)

    return None

