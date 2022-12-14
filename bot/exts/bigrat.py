from random import randint, shuffle

import discord as dc
import discord.ui as ui
import discord.ext.commands as cmds

from bot.bot import _Bot
from bot.constants import emojis


class BoxButton(ui.Button):
    def __init__(self, has_hat=False):
        super().__init__(style=dc.ButtonStyle.gray, emoji=emojis["gift"])

        self.has_hat = has_hat

    async def callback(self, interaction: dc.Interaction):
        if interaction.user.id != self.view.player.id:
            return await interaction.response.send_message(
                "This is not for you, run `/bigrat` to play.", ephemeral=True
            )

        await interaction.response.defer()

        self.show_hidden()  # Show the box content

        if self.has_hat:
            self.style = dc.ButtonStyle.success
            await self.view.won()
        else:
            self.style = dc.ButtonStyle.danger
            await self.view.lost()

        return await super().callback(interaction)

    def show_hidden(self):
        for i in self.view.children:
            if i.has_hat:
                i.emoji = emojis["xmas-hat"]
            else:
                i.emoji = None
                i.label = "\u2800"


class Bigrat(ui.View):
    def __init__(self, *, player: dc.User, bot):
        super().__init__(timeout=90)

        self.bot = bot
        self.player = player

    def remove_session(self):
        if self.player.id in self.bot.on_going_bigrat:
            self.bot.on_going_bigrat.remove(self.player.id)

        self.disable_all_items()
        self.stop()

    async def on_timeout(self):
        self.remove_session()

        for child in self.children:
            child.disabled = True

        await self.message.edit(
            view=self, embed=dc.Embed(title="Timed out.", color=0x2F3136)
        )

    async def lost(self):
        """Called when the player chose the wrong button"""
        self.remove_session()

        score = 75
        score_msg = f"{emojis['minus']} {score}xp"

        await self.bot.db.update_user_score(self.player.id, -score)

        lose_embed = dc.Embed(title="You lost :-(", description=score_msg, color=0x2F3136)
        lose_embed.set_image(url="attachment://bigrat.png")

        await self.message.edit(embed=lose_embed, view=self)

    async def won(self):
        """Called when the player clicks the right button"""
        self.remove_session()

        score = randint(400, 500)
        score_msg = f"{emojis['plus']} {score}xp"

        await self.bot.db.update_user_score(self.player.id, score)

        hat_bigrat_img = dc.File("bot/assets/bigrat-christmas-hat.png")

        win_embed = dc.Embed(title="You guessed right!", description=score_msg, color=0x2F3136)
        win_embed.set_image(url="attachment://bigrat-christmas-hat.png")

        return await self.message.edit(embed=win_embed, view=self, file=hat_bigrat_img)


class BigratCommand(dc.Cog):
    def __init__(self, bot):
        self.bot = bot

    @dc.command(name="bigrat")
    @cmds.cooldown(1, 3, cmds.BucketType.member)
    async def bigrat_cmd(self, ctx: dc.ApplicationContext):
        """Play with bigrat :D"""
        if ctx.author.id in self.bot.on_going_bigrat:
            return await ctx.respond(
                "You already have an on going `bigrat` game...", ephemeral=True
            )
        self.bot.on_going_bigrat.append(ctx.author.id)

        view = Bigrat(player=ctx.author, bot=self.bot)

        buttons = [BoxButton() for _ in range(3)]
        buttons.append(BoxButton(True))

        shuffle(buttons)

        for i in buttons:
            view.add_item(i)

        bigrat_img = dc.File("bot/assets/bigrat.png")

        bigrat_embed = dc.Embed(
            title="Guess what box contains bigrat's hat :thinking:", color=0x2F3136
        )

        bigrat_embed.set_image(url="attachment://bigrat.png")

        await ctx.respond(embed=bigrat_embed, view=view, file=bigrat_img)


def setup(bot: _Bot):
    bot.add_cog(BigratCommand(bot))
