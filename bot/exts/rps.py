import discord as dc
import discord.ui as ui

from bot.constants import emojis
from bot.bot import _Bot


class RPS(ui.View):

    def __init__(self, players: list[dc.Member], bot: _Bot) -> None:
        super().__init__()

        self.players: list[dc.Member] = players
        self.bot: _Bot = bot

        # 1: rock, 2: paper, 3: scissors.
        self.choices: dict[dc.Member, int] = {
            players[0]: 0,
            players[1]: 0
        }

        # to check if the player has played.
        self.played: dict[dc.Member, bool] = {
            players[0]: False,
            players[1]: False
        }

    def choice(self, player: dc.Member) -> str:
        _choice = self.choices[player]

        result: str = None

        if _choice == 1:
            result = "rock"
        elif _choice == 2:
            result = "paper"
        else:
            result = "scissors"

    @ui.button(label="Rock", emoji=emojis['rock'], style=dc.ButtonStyle.primary)
    async def rock(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user in self.players:
            return await interaction.response.send_message("This is not for you, run `/rps` to play.", ephemeral=True)

        if not self.played[interaction.user]:
            self.choices[interaction.user] = 1

        else:
            await interaction.response.send_message(f"You already chose [{self.choice(interaction.user)}]", ephemeral=True)

    @ui.button(label="Paper", emoji=emojis['paper'], style=dc.ButtonStyle.primary)
    async def paper(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user in self.players:
            return await interaction.response.send_message("This is not for you, run `/rps` to play.", ephemeral=True)

    @ui.button(label="Scissors", emoji=emojis['scissors'], style=dc.ButtonStyle.primary)
    async def scissors(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user in self.players:
            return await interaction.response.send_message("This is not for you, run `/rps` to play.", ephemeral=True)


class RpsCommand(dc.Cog):
    def __init__(self, bot: _Bot) -> None:
        self.bot: _Bot = bot

    @dc.command(name="rps")
    @dc.option("player", dc.Member)
    async def rps_cmd(self, ctx: dc.ApplicationContext, player: dc.Member):
        view = RPS(players=[ctx.author, player], bot=self.bot)

        game_embed = dc.Embed(color=0x2F3136)

        for player in view.players:
            game_embed.add_field(name=player.display_name, value="*thinking...*")

        await ctx.respond(embed=game_embed, view=view)


def setup(bot: _Bot) -> None:
    bot.add_cog(RpsCommand(bot))
