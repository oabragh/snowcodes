from discord import ApplicationContext, command, Embed, Cog

from bot.bot import _Bot


class Help(Cog):
    def __init__(self, bot: _Bot):
        self.bot = bot

    @command(name="help", guild_ids=[1041363391790465075])
    async def help_cmd(self, ctx: ApplicationContext):
        desc = (
            "`/balance` Check your balance!\n"
            "`/inventory` Check your inventry\n"
            "`/profile` Show your profile.\n"
            "`/gift` Gift items to your friends!\n"
            "`/pay` Send money from your wallet.\n"
            "`/among-us` Among us mini-game :D\n"
            "`/guess` Small item guessing-game"
        )

        help_embed = Embed(
            title="Santa's commands:",
            description=desc,
            colour=0x2F3136,
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )

        if av := self.bot.user.avatar:
            help_embed.set_thumbnail(url=av.url)

        help_embed.set_footer(text="merry christmas :)")

        await ctx.respond(embed=help_embed)


def setup(bot: _Bot):
    bot.add_cog(Help(bot))
