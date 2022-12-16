from random import choice, shuffle

import discord as dc
from discord import ButtonStyle, Embed, Interaction, User
from discord.ui import Button, View

from bot.bot import _Bot
from bot.constants import emojis


class AmongieButton(Button):
    def __init__(self, impostor=False):
        super().__init__(style=ButtonStyle.gray)  # Emoji is added later

        self.impostor = impostor

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.view.player.id:
            return await interaction.response.send_message(
                "This is not for you, run `/among-us` to play.", ephemeral=True
            )

        await interaction.response.defer()

        if self.impostor:
            self.style = ButtonStyle.danger

            await self.view.lost()

        else:
            self.style = ButtonStyle.success
            self.disabled = True

            await self.view.update()

        return await super().callback(interaction)


class Amongus(View):

    _score = 0
    _win_bonus = 0  # you get this when you win, default to 0

    def __init__(self, *, player: User, bot, impostors: int):
        super().__init__(timeout=30, disable_on_timeout=True)

        self.bot = bot
        self.player = player
        self.impostors = impostors

    async def lost(self):
        """Called when pressing an impostor button"""

        await self.bot.db.update_user_score(self.player.id, self.reward - 250)

        lose_embed = Embed(title="You lost!", color=0x2F3136)
        lose_embed.add_field(name="Score", value=self._score)
        lose_embed.add_field(name="XP", value=f"{self.reward-250}xp")
        lose_embed.add_field(
            name="Impostors",
            value=" ".join(  # value = every impostor button's emoji
                [str(b.emoji) for b in self.children if b.impostor]
            ),
        )

        lose_embed.set_image(url="attachment://red-line.jpg")

        self.disable_all_items()
        self.stop()

        await self.message.edit(
            content=None,
            embed=lose_embed,
            view=None,
            file=dc.File("bot/assets/red-line.jpg"),
        )

    async def update(self):
        """Update the message with the current score"""
        self._score += 1

        if self._score == 10 - self.impostors:  # If every crewmate button is clicked
            self._win_bonus = 50000

            await self.bot.db.update_user_score(self.player.id, self.reward)

            win_embed = Embed(title="You won!", color=0x2F3136)
            win_embed.add_field(name="Score", value=self._score)
            win_embed.add_field(name="XP", value=f"{self.reward}xp")
            win_embed.set_image(url="attachment://green-line.jpg")

            return await self.message.edit(
                content=None,
                embed=win_embed,
                view=None,
                file=dc.File("bot/assets/green-line.jpg"),
            )

        await self.message.edit(content=self.msg, view=self)

    @property
    def msg(self) -> int:
        """the current score state"""
        return (
            "Click on crewmates (if you pick an impostor you lose...)\n"
            f"Current score: {self._score} ({self.reward}xp)"
        )

    @property
    def reward(self) -> int:
        """Returns the reward depending on the current score"""
        result = self._score * (self.impostors * 750) + self._win_bonus

        return result


class AmongusCommand(dc.Cog):
    def __init__(self, bot):
        self.bot = bot

    @dc.command(name="among-us", guild_ids=[1041363391790465075, 1051567321535225896])
    @dc.option(
        "impostors",
        description="Higher is harder but you get more rewards",
        choices=["2", "3", "4", "5"],
    )
    async def amongus_cmd(self, ctx: dc.ApplicationContext, impostors: int):
        """Play Among us based mini-game"""

        view = Amongus(player=ctx.author, bot=self.bot, impostors=impostors)

        impostor_btns = [AmongieButton(True) for _ in range(impostors)]
        crewmate_btns = [AmongieButton() for _ in range(10 - impostors)]
        buttons = crewmate_btns + impostor_btns

        used_emojis = []
        amongies = emojis["amongies"]

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


def setup(bot: _Bot):
    bot.add_cog(AmongusCommand(bot))
