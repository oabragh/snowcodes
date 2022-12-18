import discord as dc
import discord.ext.commands as cmds

from bot.bot import _Bot


class StatsCommands(dc.Cog):
    def __init__(self, bot: _Bot) -> None:
        self.bot = bot

    @dc.command(name="leaderboard")
    @cmds.cooldown(1, 3, cmds.BucketType.member)
    async def lb_cmd(self, ctx: dc.ApplicationContext):
        """Shows the top 10 players globally"""
        players = await self.bot.db.get_all_stats()

        if not players:  # If no players are stored
            return await ctx.respond("Leaderboard is empty...", ephemeral=True)

        # Sort by xp
        players = sorted(players, key=lambda x: x[1], reverse=True)

        # If players count is more than 10 then shrink list first 10 players
        if len(players) > 10:
            players = players[:9]

        players = {
            self.bot.get_user(int(p[0])).mention: p[1]
            for p in players
        }

        ranks_column = "\n".join(str(i+1) for i in range(len(players)))
        players_column = "\n".join(i for i in players.keys())
        xp_column = "\n".join(str(i) for i in players.values())

        embed = dc.Embed(title="Leaderboard", color=0x2F3136)
        embed.set_thumbnail(url="attachment://podium.png")

        embed.add_field(name="Rank", value=ranks_column)
        embed.add_field(name="Player", value=players_column)
        embed.add_field(name="XP", value=xp_column)

        await ctx.respond(embed=embed, file=dc.File("bot/assets/podium.png"))


def setup(bot: _Bot):
    bot.add_cog(StatsCommands(bot))
