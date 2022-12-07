from discord.ext.commands import Cog
from bot.bot import _Bot

from discord import ApplicationContext, slash_command

class Debug(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="ping", guild_ids=[1041363391790465075])
    async def ping(self, inter: ApplicationContext):
        """Show the bot's latency"""
        await inter.respond(f"Pong `{round(self.bot.latency * 1000)}ms`")

def setup(bot: _Bot):
    bot.add_cog(Debug(bot))