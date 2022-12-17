import discord as dc
import discord.ext.commands as cmds

from bot.bot import _Bot


class StatsCommands(dc.Cog):
    def __init__(self, bot: _Bot) -> None:
        self.bot = bot

    @dc.command(name="profile", guild_ids=[1041363391790465075, 1051567321535225896])
    @dc.option("player", dc.Member)
    @cmds.cooldown(1, 3, cmds.BucketType.member)
    async def profile_cmd(self, ctx: dc.ApplicationContext, player: dc.Member = None):
        player = player or ctx.author

        _, score = await self.bot.db.get_user_stats(player.id)

        await ctx.respond(f"Score: {score}")


def setup(bot: _Bot):
    bot.add_cog(StatsCommands(bot))
