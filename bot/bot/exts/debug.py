from nextcord.ext.commands import Cog
from bot.bot import _Bot

from nextcord import Interaction, slash_command

class Debug(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command("ping", guild_ids=[1041363391790465075])
    async def ping(self, inter: Interaction):
        """Show the bot's latency"""
        await inter.send(f"Pong `{round(self.bot.latency * 1000)}ms`")

def setup(bot: _Bot):
    bot.add_cog(Debug(bot))