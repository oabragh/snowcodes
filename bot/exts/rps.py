import typing as t
from random import randint

import discord as dc
import discord.ui as ui
import discord.ext.commands as cmds

from bot.bot import _Bot
from bot.constants import emojis


class RPS(ui.View):
    def __init__(self, players: t.List[dc.Member], bot: _Bot) -> None:
        super().__init__(timeout=90)

        self.players: list[dc.Member] = players
        self.bot: _Bot = bot

        # 1: rock, 2: paper, 3: scissors.
        self.choices: t.Dict[dc.Member, int] = {players[0]: 0, players[1]: 0}

        # to check if the player has played.
        self.played: t.Dict[dc.Member, bool] = {players[0]: False, players[1]: False}

    async def on_timeout(self):
        self.remove_session()

        for child in self.children:
            child.disabled = True

        await self.message.edit(
            view=None, embed=dc.Embed(title="Timed out.", color=0x2F3136)
        )

    def remove_session(self):
        for i in self.players:
            if i in self.bot.on_going_rps:
                self.bot.on_going_rps.remove(i.id)

    def choice(self, player: dc.Member) -> str:
        """Returns the player's choice"""
        _choice = self.choices[player]

        result: str = None

        if _choice == 1:
            result = emojis["rock"]
        elif _choice == 2:
            result = emojis["paper"]
        else:
            result = emojis["scissors"]

        return result

    def winner(self):
        """Game logic function"""
        fi = self.choices[self.players[0]]  # first choice
        se = self.choices[self.players[1]]  # second choice
        result = None

        reversed_choices = {val: key for key, val in self.choices.items()}

        if fi == 1 and se == 2 or fi == 2 and se == 1:
            result = (reversed_choices[2], reversed_choices[1])

        if fi == 2 and se == 3 or fi == 3 and se == 2:
            result = (reversed_choices[3], reversed_choices[2])

        if fi == 3 and se == 1 or fi == 1 and se == 3:
            result = (reversed_choices[1], reversed_choices[3])

        if fi == se:
            result = 0

        return result

    @property
    def game_embed(self) -> dc.Embed:
        desc = ""

        for player in self.players:
            if self.played[player]:
                has_played = ":white_check_mark: played."
            else:
                has_played = "*thinking*"

            desc += f"{player.mention}: {has_played}\n"

        embed = dc.Embed(title="RPS game started.", color=0x2F3136, description=desc)

        return embed

    async def choose(self, inter: dc.Interaction, choice: int) -> None:
        """Sets a player's choice and updates the game embed"""
        if not self.played[inter.user]:
            self.choices[inter.user] = choice
            self.played[inter.user] = True

        else:
            return await inter.response.send_message(
                f"You already chose {self.choice(inter.user)}", ephemeral=True
            )

        await inter.response.defer()

        if [i for i in self.played.values()] == [True, True]:
            self.disable_all_items()
            self.stop()

            async def tie():
                embed = dc.Embed(
                    title="Game ended with a tie!",
                    description=f"You both chose {self.choice(inter.user)}",
                    color=0x2F3136,
                )
                embed.set_image(url="attachment://red-line.jpg")
                await self.message.edit(
                    content=None,
                    view=None,
                    embed=embed,
                    file=dc.File("bot/assets/red-line.jpg"),
                )

            async def win(result):
                winner, loser = result

                winner_xp = randint(500, 1000)
                loser_xp = 50

                # Update scores
                await self.bot.db.update_user_score(winner.id, winner_xp)
                await self.bot.db.update_user_score(loser.id, -loser_xp)

                score = f"{emojis['plus']} {winner_xp}xp: {winner.mention} ({self.choice(winner)})\
                        \n{emojis['minus']} {loser_xp}xp: {loser.mention} ({self.choice(loser)})"

                embed = dc.Embed(
                    title="Game ended.",
                    description=f"{winner.mention} won the game!",
                    color=0x2F3136,
                )
                embed.set_image(url="attachment://green-line.jpg")
                embed.add_field(name="Score:", value=score)

                await self.message.edit(
                    content=None,
                    view=None,
                    embed=embed,
                    file=dc.File("bot/assets/green-line.jpg"),
                )

            if self.winner() == 0:
                await tie()

            else:
                await win(self.winner())

            self.remove_session()
        else:
            await self.message.edit(embed=self.game_embed)

    @ui.button(label="Rock", emoji=emojis["rock"], style=dc.ButtonStyle.primary)
    async def rock(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user in self.players:
            return await interaction.response.send_message(
                "This is not for you, run `/rps` to play.", ephemeral=True
            )

        await self.choose(interaction, 1)

    @ui.button(label="Paper", emoji=emojis["paper"], style=dc.ButtonStyle.primary)
    async def paper(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user in self.players:
            return await interaction.response.send_message(
                "This is not for you, run `/rps` to play.", ephemeral=True
            )

        await self.choose(interaction, 2)

    @ui.button(label="Scissors", emoji=emojis["scissors"], style=dc.ButtonStyle.primary)
    async def scissors(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user in self.players:
            return await interaction.response.send_message(
                "This is not for you, run `/rps` to play.", ephemeral=True
            )

        await self.choose(interaction, 3)


class RpsCommand(dc.Cog):
    def __init__(self, bot: _Bot) -> None:
        self.bot: _Bot = bot

    @dc.command(name="rps")
    @dc.option("player", dc.Member)
    @cmds.cooldown(1, 3, cmds.BucketType.member)
    async def rps_cmd(self, ctx: dc.ApplicationContext, player: dc.Member):
        if player == ctx.author or player.bot:
            return await ctx.respond(
                "You can't play with yourself or a bot.", ephemeral=True
            )

        playing = []

        if self.author.id in self.bot.on_going_rps:
            playing.append("You")

        if player.id in self.bot.on_going_rps:
            playing.append(self.author.mention)

        if playing:
            players = " and ".join(playing)
            return await inter.response.send_message(
                f"{players} already have an ongoing `rps` game...", ephemeral=True
            )

        self.bot.on_going_rps.extend([self.author.id, inter.user.id])

        view = RPS(players=[ctx.author, player], bot=self.bot)

        await ctx.respond(embed=view.game_embed, view=view)


def setup(bot: _Bot) -> None:
    bot.add_cog(RpsCommand(bot))
