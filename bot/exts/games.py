from random import shuffle, choice

from discord import (ApplicationContext, Member, Embed, File, Cog, option,
                     command)
from bot.bot import _Bot
from bot.constants import emojis
from bot.exts.amongus.button import AmongieButton
from bot.exts.amongus.view import Amongus
from bot.exts.bigrat.button import BoxButton
from bot.exts.bigrat.view import Bigrat
from bot.exts.duel.view import DuelInvite

class Games(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="among-us", guild_ids=[1041363391790465075, 1051567321535225896])
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

    @command(name="bigrat", guild_ids=[1041363391790465075, 1051567321535225896])
    async def bigrat_cmd(self, ctx: ApplicationContext):
        """Play with bigrat :D"""
        view = Bigrat(player=ctx.author, bot=self.bot)

        buttons = [BoxButton() for _ in range(3)]
        buttons.append(BoxButton(True))

        shuffle(buttons)

        for i in buttons:
            view.add_item(i)

        bigrat_img = File("bot/assets/bigrat.png")

        bigrat_embed = Embed(
            title="Guess what box contains bigrat's hat :thinking:",
            color=0x2F3136
        )

        bigrat_embed.set_image(url="attachment://bigrat.png")

        await ctx.respond(embed=bigrat_embed, view=view, file=bigrat_img)

    @command(name="duel", guild_ids=[1041363391790465075, 1051567321535225896])
    @option("player", Member)
    @option("bet", int, required=False)
    async def duel_cmd(self, ctx: ApplicationContext, player: Member, bet: int = None):
        _, player_wallet, _, _ = await self.bot.db.get_user_balance(player.id)
        _, your_wallet, _, _ = await self.bot.db.get_user_balance(ctx.author.id)

        bet_msg = ""

        if bet:
            if player_wallet < bet:
                return await ctx.respond(f"{player.mention} Doesn't have that amount.")

            elif your_wallet < bet:
                return await ctx.respond(f"You don't have that amount.")

            bet_msg = f"for {bet} {emojis['currency']}"

        invite_embed = Embed(title="Do you accept challenge?",
                             description=f"{ctx.author.mention} invited you to a duel {bet_msg}",
                             color=0x2F3136)
        invite_embed.set_footer(text="you have 60s to respond.")

        duel = DuelInvite(player=player, author=ctx.author, bet=bet)

        await ctx.respond(
            player.mention,
            embed=invite_embed,
            view=duel
        )


def setup(bot: _Bot):
    bot.add_cog(Games(bot))
