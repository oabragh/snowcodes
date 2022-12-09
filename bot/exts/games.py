from random import shuffle

from discord import option, slash_command, ApplicationContext, Embed, Colour
from discord.ext.commands import Cog

from bot.bot import _Bot
from bot.exts.amongus.button import AmongieButton
from bot.exts.amongus.view import Amongus

from bot.exts.bigrat.view import Bigrat
from bot.exts.bigrat.button import BoxButton


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

        view = Amongus(player=ctx.author, bot=self.bot, impostors=impostors)

        impostor_btns = [AmongieButton(True) for _ in range(impostors)]
        crewmate_btns = [AmongieButton() for _ in range(10 - impostors)]
        buttons = crewmate_btns + impostor_btns

        shuffle(buttons)  # Randomize impostor buttons index

        for i in buttons:
            view.add_item(i)

        await ctx.respond(view.msg, view=view)

    @slash_command(name="bigrat", guild_ids=[1041363391790465075])
    async def bigrat_cmd(self, ctx: ApplicationContext):
        """Play with bigrat"""

        view = Bigrat(player=ctx.author, bot=self.bot)

        buttons = [BoxButton() for _ in range(3)]
        buttons.append(BoxButton(True))

        shuffle(buttons)

        for i in buttons:
            view.add_item(i)

        bigrat_embed = Embed(title="Guess what box contains bigrat's hat :thinking:",
                             color=Colour.blurple())

        bigrat_embed.set_image(url="attachment://bigrat.png")

        await ctx.respond(embed=bigrat_embed, view=view, file=view.bigrat_img)


def setup(bot: _Bot):
    bot.add_cog(Games(bot))
