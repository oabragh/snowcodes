from discord import ApplicationContext, slash_command, Member, option
from discord.ext.commands import Cog

from bot.bot import _Bot


class Debug(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.helper = self.bot.dbh

    @slash_command(name="ping", guild_ids=[1041363391790465075])
    async def ping(self, ctx: ApplicationContext):
        """Show the bot's latency"""
        await ctx.respond(f"Pong `{round(self.bot.latency * 1000)}ms`")

    @slash_command(name="give-coins", guild_ids=[1041363391790465075])
    @option("user", Member)
    @option("amount", int)
    async def give_cmd(self, ctx: ApplicationContext, user: Member, amount: int):
        await self.helper.update_user_wallet(user.id, amount)
        await ctx.respond("done")


def setup(bot: _Bot):
    bot.add_cog(Debug(bot))
