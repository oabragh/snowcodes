import discord as dc
import discord.ext.commands as cmds

from bot.bot import _Bot


class StatsCommands(dc.Cog):
    def __init__(self, bot: _Bot) -> None:
        self.bot = bot

    @dc.command(
        name="leaderboard", guild_ids=[1041363391790465075, 1051567321535225896]
    )
    @cmds.cooldown(1, 3, cmds.BucketType.member)
    async def lb_cmd(self, ctx: dc.ApplicationContext):
        players = await self.bot.db.get_all_stats()

        if not players:  # If no players are stored
            return await ctx.respond("Leaderboard is empty...", ephemeral=True)

        # Sort by xp
        players = sorted(players, key=lambda x: x[1], reverse=True)

        # If players count is more than 10 then shrink list first 10 players
        if len(players) > 10:
            players = players[:9]

        desc = ""

        # For each player, add them in description
        for idx, i in enumerate(players):
            desc += f"{idx+1}. {self.bot.get_user(int(i[0])).mention}: `{i[1]}xp`\n"

        embed = dc.Embed(title="Leaderboard", description=desc, color=0x2F3136)
        await ctx.respond(embed=embed)


def setup(bot: _Bot):
    bot.add_cog(StatsCommands(bot))