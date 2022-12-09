from discord import ButtonStyle, Interaction
from discord.ui import Button


class AmongieButton(Button):
    def __init__(self, impostor=False):
        super().__init__(style=ButtonStyle.gray, emoji="🙍‍♂️")

        self.impostor = impostor

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.view.player.id:
            return await interaction.response.send_message(
                "This is not for you, run `/among-us` to play.", ephemeral=True
            )

        if self.impostor:
            self.style = ButtonStyle.danger

            await interaction.response.defer()
            await self.view.lost()

        else:
            self.style = ButtonStyle.success
            self.disabled = True

            await interaction.response.defer()
            await self.view.update()

        return await super().callback(interaction)
