import typing as t
from random import choice, randint

from discord import ButtonStyle, Embed, Interaction, Member
from discord.ui import Button, View, button

from bot.constants import emojis


class Duel(View):
    action = None

    def __init__(self, players: t.List[Member], bet: int):
        super().__init__(timeout=60, disable_on_timeout=True)

        self.bet = bet
        self.players = players
        self.current_player = choice(self.players)
        self.next_player = [
            i for i in self.players if not i == self.current_player][0]

        self.stats = {
            self.players[0]: {
                "name": self.players[0].display_name,
                "health": 100,
                "shield": 0
            },
            self.players[1]: {
                "name": self.players[1].display_name,
                "health": 100,
                "shield": 0
            }
        }

    @property
    def game_embed(self):
        em = Embed(title=" vs ".join(
            [m.display_name for m in self.players]), color=0x2F3136)
        for i in self.stats.values():
            em.add_field(
                name=i['name'], value=f"Health: {i['health']}/100 :heart:\nShield: {i['shield']}/100 :shield:")

        if self.action:
            em.description = self.action

        return em

    def swap(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    async def update(self):
        await self.message.edit(content=f"{self.current_player.mention}, Its your turn.", embed=self.game_embed)

    async def won(self, player: Member):

        reward = ""

        if self.bet:
            reward = f"for {self.bet*2} {emojis['currency']}"

        win_embed = Embed(
            title="Duel finished.",
            description=f"{self.current_player.mention} Won {self.next_player.mention} {reward}",
            color=0X2F3136)

        win_embed .add_field(name="Reward", value="nothing heh")
        await self.message.edit(content=f"{self.current_player.mention} Won the battle!", embed=win_embed, view=None)

        self.stop()

    @button(label="Throw Snowball")
    async def punch(self, button: Button, interaction: Interaction):
        if not interaction.user.id == self.current_player.id:
            return await interaction.response.send_message("It's not your turn.", ephemeral=True)

        await interaction.response.defer()

        damage = randint(5, 15)

        self.stats[self.next_player]["health"] -= damage

        if self.stats[self.next_player]["health"] <= 0:
            return await self.won(self.current_player)

        self.action = f"{self.current_player.mention} threw a snowball on {self.next_player.mention} dealing {damage} damage!"
        self.swap()
        await self.update()

    @button(label="Kick")
    async def kick(self, button: Button, interaction: Interaction):
        if not interaction.user.id == self.current_player.id:
            return await interaction.response.send_message("It's not your turn.", ephemeral=True)

        await interaction.response.defer()

        damage = randint(0, 32)

        self.stats[self.next_player]["health"] -= damage

        if self.stats[self.next_player]["health"] <= 0:
            return await self.won(self.current_player)

        self.action = f"{self.current_player.mention} kicked {self.next_player.mention} dealing {damage} damage!"

        if damage == 0:
            self.action = f"{self.current_player.display_name} tried to kick but FELL DOWN!"

        self.swap()
        await self.update()

    @button(label="Upgrade Defense", style=ButtonStyle.primary)
    async def defend(self, button: Button, interaction: Interaction):
        if not interaction.user.id == self.current_player.id:
            return await interaction.response.send_message("It's not your turn.", ephemeral=True)

        await interaction.response.defer()

        upgrade = randint(5, 25)
        self.stats[self.current_player]["shield"] += upgrade

        self.action = f"{self.current_player.mention} upgraded their defense!"
        self.swap()
        await self.update()


class DuelInvite(View):
    def __init__(self, player: Member, author: Member, bet: int):
        super().__init__(timeout=60, disable_on_timeout=True)

        self.author = author
        self.player = player
        self.bet = bet

    @button(label="Accept", style=ButtonStyle.success)
    async def accept(self, button: Button, interaction: Interaction):
        if not interaction.user.id == self.player.id:
            return await interaction.response.send_message("This is not for you.", ephemeral=True)
        self.stop()

        await self.start_duel(interaction)

    @button(label="Reject", style=ButtonStyle.danger)
    async def reject(self, button: Button, interaction: Interaction):
        if not interaction.user.id == self.player.id:
            return await interaction.response.send_message("This is not for you.", ephemeral=True)
        self.disable_all_items()
        self.stop()

        reject_embed = Embed(title="Duel rejected.", color=0x2F3136)
        await interaction.response.edit_message(embed=reject_embed, view=self)

    async def start_duel(self, inter):
        view = Duel(players=[self.author, self.player], bet=self.bet)

        await inter.response.send_message(f"{view.current_player.mention}, It's your turn.", embed=view.game_embed, view=view)
