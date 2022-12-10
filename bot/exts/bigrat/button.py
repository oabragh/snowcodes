from discord import ButtonStyle, Interaction
from discord.ui import Button

from bot.constants import emojis


class BoxButton(Button):
    def __init__(self, has_hat=False):
        super().__init__(style=ButtonStyle.gray, emoji=emojis["gift"])

        self.has_hat = has_hat

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.view.player.id:
            return await interaction.response.send_message(
                "This is not for you, run `/bigrat` to play.",
                ephemeral=True)

        await interaction.response.defer()

        self.show_hidden()  # Show the box content

        if self.has_hat:
            self.style = ButtonStyle.success
            await self.view.won()
        else:
            self.style = ButtonStyle.danger
            await self.view.lost()

        return await super().callback(interaction)

    def show_hidden(self):
        for i in self.view.children:
            if i.has_hat:
                i.emoji = emojis["xmas-hat"]
            else:
                i.emoji = None
                i.label = "\u2800"
