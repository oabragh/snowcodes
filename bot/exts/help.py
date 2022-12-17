from discord import ApplicationContext, Cog, Embed, File, command
import discord.ext.commands as cmds
import discord as dc

from bot.bot import _Bot


class Help(Cog):
    def __init__(self, bot: _Bot):
        self.bot = bot

    @command(name="help", guild_ids=[1041363391790465075, 1051567321535225896])
    async def help_cmd(self, ctx: ApplicationContext):
        """Shows you how to use the bot"""
        desc = (
            "`/among-us` Among us mini-game :D\n"
            "`/balance` Check your balance!\n"
            "`/bigrat` Play with bigrat\n"
            "`/deposit` Deposit to your vault\n"
            "`/pay` Send money from your wallet.\n"
            "`/withdraw` Withdraw from your vault\n"
        )

        help_embed = Embed(
            title="Santa's commands:",
            description=desc,
            colour=0x2F3136,
            url="https://discord.gg/ggZn8PaQed",
        )

        help_embed.set_thumbnail(url="attachment://question.png")
        help_embed.set_footer(text="merry christmas :)")

        await ctx.respond(embed=help_embed, file=File("bot/assets/question.png"))


def setup(bot: _Bot):
    bot.add_cog(Help(bot))
