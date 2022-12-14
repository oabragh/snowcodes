from discord import ApplicationContext, Bot, Cog, Member, command, option


class Profile(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="profile", guild_ids=[1041363391790465075, 1051567321535225896])
    @option("player", Member)
    async def player_cmd(self, ctx: ApplicationContext, player: Member = None):
        player = player or ctx.author

        _, score = await self.bot.db.get_user_stats(player.id)

        await ctx.respond(f"Score: {score}")


def setup(bot: Bot):
    bot.add_cog(Profile(bot))
