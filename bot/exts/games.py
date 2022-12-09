from random import shuffle, choice

from discord import (ApplicationContext, Colour, Embed, File, option,
                     command)
from discord.ext.commands import Cog
from time import time
from bot.bot import _Bot
from bot.constants import emojis
from bot.exts.amongus.button import AmongieButton
from bot.exts.amongus.view import Amongus
from bot.exts.bigrat.button import BoxButton
from bot.exts.bigrat.view import Bigrat


class Games(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="among-us", guild_ids=[1041363391790465075])
    @option(
        "impostors",
        description="Higher is harder but you get more rewards",
        choices=["2", "3", "4", "5"],
    )
    async def amongus_cmd(self, ctx: ApplicationContext, impostors: int):
        """Among us mini-game :D"""

        view = Amongus(player=ctx.author, bot=self.bot, impostors=impostors)

        impostor_btns = [AmongieButton(True) for _ in range(impostors)]
        crewmate_btns = [AmongieButton() for _ in range(10-impostors)]
        buttons = crewmate_btns + impostor_btns

        used_emojis = []
        amongies = emojis['amongies']

        for i in buttons:
            emoji = choice(amongies)
            while emoji in used_emojis:
                emoji = choice(amongies)

            i.emoji = emoji

            used_emojis.append(emoji)

        shuffle(buttons)  # Randomize impostor buttons index

        for i in buttons:
            view.add_item(i)

        await ctx.respond(view.msg, view=view)

    @command(name="bigrat", guild_ids=[1041363391790465075])
    async def bigrat_cmd(self, ctx: ApplicationContext):
        """Play with bigrat"""
        await ctx.defer()
        view = Bigrat(player=ctx.author, bot=self.bot)

        buttons = [BoxButton() for _ in range(3)]
        buttons.append(BoxButton(True))

        shuffle(buttons)

        for i in buttons:
            view.add_item(i)

        bigrat_img = File("bot/assets/bigrat.png")

        bigrat_embed = Embed(
            title="Guess what box contains bigrat's hat :thinking:",
            color=Colour.blurple()
        )

        bigrat_embed.set_image(url="attachment://bigrat.png")

        await ctx.respond(embed=bigrat_embed, view=view, file=bigrat_img)


def setup(bot: _Bot):
    bot.add_cog(Games(bot))
