from discord.ui import Button
from discord import Interaction, ButtonStyle

class TicTacToeButton(Button):
    def __init__(self, x: int, y: int):
        super().__init__(label="\u2800", row=y)

        self.x = x
        self.y = y

    async def callback(self, interaction: Interaction):
        if interaction.user not in self.view.players.keys():
            return await interaction.response.send_message("This is not for you, run `/tictactoe` to play.", ephemeral=True)

        if interaction.user.id != self.view.current_player.id:
            return await interaction.response.send_message("It's not your turn", ephemeral=True)

        await interaction.response.defer()

        self.style = ButtonStyle.primary
        self.label = self.view.players[interaction.user]

        self.view.board[self.x, self.y] = self.view.players[interaction.user]

        for i in self.view.players.keys():
            if not i == interaction.user:
                self.view.current_player = i

        return await super().callback(interaction)
