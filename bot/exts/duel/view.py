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
        em = Embed(color=0x2F3136)
        for i in self.stats.values():
            em.add_field(
                name=i['name'], value=f"Health: {i['health']}/100 :heart:\nShield: {i['shield']}/100 :shield:")

        if not self.action:
            self.action = "Battle started!"

        em.add_field(name="Last Action", value=f"`{self.action}`", inline=False)

        return em

    def swap(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    async def update(self):
        await self.message.edit(content=f"{self.current_player.mention}, Its your turn.", embed=self.game_embed)

    async def damage(self, player, amount):
        shield = (self.stats[player]["shield"]/100)*100
        self.stats[player]["health"] -= (amount)

        if self.stats[player]["health"] < 0:
            self.stats[player]["health"] = 0

            return True

        return False

    async def won(self, winner: Member, loser: Member):
        win_embed = Embed(
            title="Duel finished.",
            description=f"{self.current_player.mention} beat {self.next_player.mention}! :flex:",
            color=0X2F3136)

        if self.bet:
            win_embed.add_field(
                name="Reward", value=f"{self.bet*2} {emojis['currency']}")
            
            await self.bot.db.update_user_wallet(winner.id, self.bet*2)
            await self.bot.db.update_user_wallet(loser.id, -self.bet)
            

        await self.message.edit(content=None, embed=win_embed, view=None)

        self.stop()
    
    @button(label="Punch", emoji=emojis['punch'])
    async def punch(self, button: Button, interaction: Interaction):
        if not interaction.user.id == self.current_player.id:
            return await interaction.response.send_message("It's not your turn.", ephemeral=True)

        await interaction.response.defer()

        damage = randint(5, 20)

        result = await self.damage(self.next_player, damage)

        if result:
            return await self.won(self.current_player, self.next_player)

        self.action = f"{self.current_player.display_name} punched {self.next_player.display_name} dealing {damage} damage!"

        self.swap()
        await self.update()

    @button(label="Snowball Attack", emoji=emojis['snowball'])
    async def snowball(self, button: Button, interaction: Interaction):
        if not interaction.user.id == self.current_player.id:
            return await interaction.response.send_message("It's not your turn.", ephemeral=True)

        await interaction.response.defer()

        dmg = randint(6, 32)
        choices = [dmg, dmg, 0, dmg, dmg]

        damage = choice(choices)

        self.action = f"{self.current_player.display_name} threw a snowball on {self.next_player.display_name} dealing {damage} damage!"

        if damage == 0:
            self.action = f"{self.current_player.display_name} tried to throw snowball but his aim sucks!"

        result = await self.damage(self.next_player, damage)

        if result:
            return await self.won(self.current_player, self.next_player)

        self.swap()
        await self.update()

    @button(label="Upgrade Defense", style=ButtonStyle.primary, emoji=emojis['shield'])
    async def defend(self, button: Button, interaction: Interaction):
        if not interaction.user.id == self.current_player.id:
            return await interaction.response.send_message("It's not your turn.", ephemeral=True)

        if self.stats[self.current_player]["shield"] == 100:
            return await interaction.response.send_message("Your shield is maxed out. try something else", ephemeral=True)

        await interaction.response.defer()

        upgrade = randint(5, 25)
        self.stats[self.current_player]["shield"] += upgrade

        if self.stats[self.current_player]["shield"] > 100:
            self.stats[self.current_player]["shield"] = 100

        self.action = f"{self.current_player.display_name} upgraded their defense!"
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
        self.disable_all_items()
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

    async def start_duel(self, inter: Interaction):
        view = Duel(players=[self.author, self.player], bet=self.bet)

        await inter.response.send_message(f"{view.current_player.mention}, It's your turn.", embed=view.game_embed, view=view)
