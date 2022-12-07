from discord import ApplicationContext, slash_command
from discord.ext.commands import Cog

from bot.bot import _Bot


class Debug(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="ping", guild_ids=[1041363391790465075])
    async def ping(self, ctx: ApplicationContext):
        """Show the bot's latency"""
        await ctx.respond(f"Pong `{round(self.bot.latency * 1000)}ms`")


def setup(bot: _Bot):
    bot.add_cog(Debug(bot))
