from discord.ext.commands import Cog
from bot.bot import _Bot

from discord import ApplicationContext, slash_command

class Help(Cog):
    def __init__(self, bot: _Bot):
        self.bot = bot

    @slash_command(name="help", guild_ids=[1041363391790465075])
    async def help_cmd(self, ctx: ApplicationContext):
        await ctx.respond("Help.")


def setup(bot: _Bot):
    bot.add_cog(Help(bot))