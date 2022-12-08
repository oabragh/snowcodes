from random import shuffle

from discord import ApplicationContext, option, slash_command
from discord.ext.commands import Cog

from bot.bot import _Bot
from bot.exts.amongus.button import AmongieButton
from bot.exts.amongus.view import Amongus


class Games(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="among-us", guild_ids=[1041363391790465075])
    @option(
        "impostors",
        description="Higher is harder but you get more rewards",
        choices=["2", "3", "4", "5"],
    )
    async def amongus_cmd(self, ctx: ApplicationContext, impostors: int):
        """Among us mini-game :D"""

        view = Amongus(ctx.author, impostors, self.bot)

        impostor_btns = [AmongieButton(True) for _ in range(impostors)]
        crewmate_btns = [AmongieButton() for _ in range(10-impostors)]
        buttons = crewmate_btns + impostor_btns

        shuffle(buttons) # Randomize impostor buttons index

        for i in buttons:
            print(i.impostor)
            view.add_item(i)

        await ctx.respond(view.msg, view=view)


def setup(bot: _Bot):
    bot.add_cog(Games(bot))
