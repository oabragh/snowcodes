from random import choice, shuffle

import discord as dc
import discord.ui as ui
import discord.ext.commands as cmds

from bot.bot import _Bot
from bot.constants import emojis


class AmongieButton(ui.Button):
    def __init__(self, impostor=False):
        super().__init__(style=dc.ButtonStyle.gray)  # Emoji is added later

        self.impostor: bool = impostor

    async def callback(self, interaction: dc.Interaction):
        if interaction.user.id != self.view.player.id:
            return await interaction.response.send_message(
                "This is not for you, run `/among-us` to play.", ephemeral=True
            )

        await interaction.response.defer()

        """
        If the clicked amongie button is an impostor, call `self.view.lost()`
        Else the button becames green and disabled.
        """

        if self.impostor:
            self.style = dc.ButtonStyle.danger

            await self.view.lost()

        else:
            self.style = dc.ButtonStyle.success
            self.disabled = True

            await self.view.update()

        return await super().callback(interaction)


class Amongus(ui.View):

    _score = 0
    _win_bonus = 0  # you get this when you win, default to 0

    def __init__(self, *, player: dc.User, bot: _Bot, impostors: int):
        super().__init__(timeout=90)

        self.bot: _Bot = bot
        self.player = player
        self.impostors = impostors

    def remove_session(self):
        if self.player.id in self.bot.on_going_amongus:
            self.bot.on_going_amongus.remove(self.player.id)

    async def on_timeout(self):
        self.remove_session()

        for child in self.children:
            child.disabled = True

        await self.bot.db.update_user_score(self.player.id, self.reward - 250)

        if not self.message:
            return

        impostors = " ".join([str(b.emoji) for b in self.children if b.impostor])
        lose_embed = dc.Embed(
            title="You took too long to respond, you lost!", color=0x2F3136
        )
        lose_embed.add_field(name="Score", value=self._score)
        lose_embed.add_field(name="XP", value=f"{self.reward-250}xp")
        lose_embed.add_field(name="Impostors", value=impostors)
        lose_embed.set_image(url="attachment://red-line.jpg")

        await self.message.edit(
            content=None,
            embed=lose_embed,
            view=None,
            file=dc.File("bot/assets/red-line.jpg"),
        )

    async def lost(self):
        """Called when pressing an impostor button"""

        self.remove_session()

        # Update the user's score.
        await self.bot.db.update_user_score(self.player.id, self.reward - 250)

        # Disable view
        self.disable_all_items()
        self.stop()

        if not self.message:  # Don't expect users to play properly....
            return  # Don't attempt to edit message.

        # Send embed

        impostors = " ".join([str(b.emoji) for b in self.children if b.impostor])
        lose_embed = dc.Embed(title="You lost!", color=0x2F3136)
        lose_embed.add_field(name="Score", value=self._score)
        lose_embed.add_field(name="XP", value=f"{self.reward-250}xp")
        lose_embed.add_field(name="Impostors", value=impostors)
        lose_embed.set_image(url="attachment://red-line.jpg")

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
            self.remove_session()
            self._win_bonus = 1000

            # Update the user's score.
            await self.bot.db.update_user_score(self.player.id, self.reward)

            win_embed = dc.Embed(title="You won!", color=0x2F3136)
            win_embed.add_field(name="Score", value=self._score)
            win_embed.add_field(name="XP", value=f"{self.reward}xp")
            win_embed.set_image(url="attachment://green-line.jpg")

            return await self.message.edit(
                content=None,
                embed=win_embed,
                view=None,
                file=dc.File("bot/assets/green-line.jpg"),
            )

        # Update view
        await self.message.edit(content=self.msg, view=self)

    @property
    def msg(self) -> int:
        """the current score state (used in the game message)"""
        return (
            "Click on crewmates (if you pick an impostor you lose...)\n"
            f"Current score: {self._score} ({self.reward}xp)"
        )

    @property
    def reward(self) -> int:
        """
        Returns the reward depending on the current score.

        every crewmate clicked * (impostors count * 750) + win bonus if you won
        """
        result = self._score * (self.impostors * 150) + self._win_bonus

        return result


class AmongusCommand(dc.Cog):
    def __init__(self, bot):
        self.bot = bot

    @dc.command(name="among-us")
    @cmds.cooldown(1, 15, cmds.BucketType.member)
    @dc.option(
        "impostors",
        description="Higher is harder but you get more rewards",
        choices=["2", "3", "4", "5"],
    )
    async def amongus_cmd(self, ctx: dc.ApplicationContext, impostors: int):
        """Play Among us based mini-game."""

        if ctx.author.id in self.bot.on_going_amongus:
            return await ctx.respond(
                "You already have an on going `among-us` game...", ephemeral=True
            )

        self.bot.on_going_amongus.append(ctx.author.id)

        view = Amongus(player=ctx.author, bot=self.bot, impostors=impostors)

        impostor_btns = [AmongieButton(True) for _ in range(impostors)]
        crewmate_btns = [AmongieButton() for _ in range(10 - impostors)]
        buttons = crewmate_btns + impostor_btns

        used_emojis = []
        amongies = emojis["amongies"]

        for i in buttons:
            emoji = choice(amongies)
            while emoji in used_emojis:  # To make sure there are no duplicated emojis
                emoji = choice(amongies)

            i.emoji = emoji

            used_emojis.append(emoji)

        shuffle(buttons)  # Randomize impostor buttons index

        for i in buttons:
            view.add_item(i)

        await ctx.respond(view.msg, view=view)

    @amongus_cmd.error
    async def amongus_error(
        self, ctx: dc.ApplicationContext, error: dc.DiscordException
    ):
        if isinstance(error, cmds.CommandOnCooldown):
            return await ctx.respond(
                f"You can play again in `{int(error.retry_after)}s`", ephemeral=True
            )

        else:
            raise error


def setup(bot: _Bot):
    bot.add_cog(AmongusCommand(bot))
