from discord import ApplicationContext, Cog, Embed, File, command
import discord.ext.commands as cmds
import discord as dc

from bot.bot import _Bot


class Help(Cog):
    def __init__(self, bot: _Bot):
        self.bot = bot

    @command(name="help")
    async def help_cmd(self, ctx: ApplicationContext):
        """Shows you how to use the bot"""
        desc = (
            "`/among-us` Among us based mini-game\n"
            "`/bigrat` Play a game with bigrat :D\n"
            "`/duel` Challenge your friend with a duel!\n"
            "`/rps` Rock Paper Scissors\n"
            "`/leaderboard` Shows the top 10 players globally\n"
        )

        help_embed = Embed(
            title="Bot's commands:",
            description=desc,
            colour=0x2F3136,
            url="https://discord.gg/ggZn8PaQed",
        )

        help_embed.set_footer(text="Merry christmas :)")

        await ctx.respond(embed=help_embed)


def setup(bot: _Bot):
    bot.add_cog(Help(bot))
