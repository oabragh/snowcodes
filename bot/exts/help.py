import discord as dc
import discord.ext.commands as cmds

from bot.bot import _Bot


class Help(dc.Cog):
    def __init__(self, bot: _Bot):
        self.bot = bot

    @dc.command(name="help")
    async def help_cmd(self, ctx: dc.ApplicationContext):
        """Shows you how to use the bot"""
        commands = {
            "/among-us": "Among us based mini-game",
            "/bigrat": "Play a game with bigrat :D",
            "/duel": "Challenge your friend with a duel!",
            "/rps": "Play Rock-Paper-Scissors",
            "/leaderboard": "Shows the top 10 players globally",
        }

        description = (
            "A game bot with 4 mini-games and a leaderboard to compete\n"
            "with others! this was made in a timespan of 10 days~ so you\n"
            "may encounter a few issues..."
        )

        help_embed = dc.Embed(
            title="What is this?",
            colour=0x2F3136,
            description=description,
            url="https://discord.gg/ggZn8PaQed",
        )

        repo = "https://github.com/oabragh/snowcodes"
        help_embed.set_author(
            icon_url=self.bot.user.avatar.url, name=self.bot.user.name, url=repo
        )

        help_embed.add_field(
            name="Command", value="\n".join([f"`{i}`" for i in commands.keys()])
        )
        help_embed.add_field(
            name="Description", value="\n".join([i for i in commands.values()])
        )
        help_embed.set_footer(text="Merry christmas ^_^ (Made by *****#5080)")

        await ctx.respond(embed=help_embed)


def setup(bot: _Bot):
    bot.add_cog(Help(bot))
