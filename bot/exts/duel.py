import typing as t
from random import choice, randint

import discord as dc
import discord.ui as ui
import discord.ext.commands as cmds

from bot.bot import _Bot
from bot.constants import emojis


class Duel(ui.View):
    action = None

    def __init__(self, players: t.List[dc.Member], bot: _Bot):
        super().__init__(timeout=90)

        self.bot: _Bot = bot

        self.players = players
        self.current_player: dc.Member = choice(self.players)
        self.next_player: dc.Member = [
            i for i in self.players if not i == self.current_player
        ][0]

        self.stats = {
            self.players[0]: {
                "name": self.players[0].display_name,
                "health": 100,
                "shield": 0,
            },
            self.players[1]: {
                "name": self.players[1].display_name,
                "health": 100,
                "shield": 0,
            },
        }

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

        await self.message.edit(embed=dc.Embed(title="Duel timed out.", color=0x2F3136))

        for i in self.players:
            if i in self.bot.on_going_duels:
                self.bot.on_going_duels.remove(i.id)

    @property
    def game_embed(self):
        """Returns the game embed."""
        embed = dc.Embed(color=0x2F3136)

        for i in self.stats.values():  # Add a field for each player
            player_health = f"Health: {i['health']}/100 :heart:"
            player_shield = f"Shield: {i['shield']}/100 :shield:"
            embed.add_field(name=i["name"], value=f"{player_health}\n{player_shield}")

        if (
            not self.action
        ):  # If no action exist, its most likely the battle just started.
            self.action = "Battle started!"

        embed.add_field(name="Last Action", value=f"`{self.action}`", inline=False)

        return embed

    def swap(self):
        """Swaps play turns after"""
        self.current_player, self.next_player = self.next_player, self.current_player

    def stop(self):
        for i in self.players:
            self.bot.on_going_duels.remove(i.id)
        super().stop()

    async def update(self):
        """Edit the game message with the current stats"""
        await self.message.edit(
            content=f"{self.current_player.mention}, Its your turn.",
            embed=self.game_embed,
        )

    async def damage(self, player, amount):
        """Damages a player and reducing depending on the shield"""
        shield = self.stats[player]["shield"]
        reduce_percentage = shield * 45 / 100

        new_damage = amount - int(amount * reduce_percentage / 100)

        self.stats[player]["health"] -= new_damage

        if self.stats[player]["health"] <= 0:  # To prevent health from being under 0
            self.stats[player]["health"] = 0

            return True  # Player has lost

        return False  # Player can still play

    async def end(self, winner: dc.Member, loser: dc.Member):
        winner_xp = randint(500, 1000)
        loser_xp = 250

        # Update scores
        await self.bot.db.update_user_score(winner.id, winner_xp)
        await self.bot.db.update_user_score(loser.id, -loser_xp)

        result = (
            f"{self.current_player.mention} won {self.next_player.mention}! :muscle:"
        )

        win_embed = dc.Embed(title="Duel finished.", description=result, color=0x2F3136)
        win_embed.set_image(url="attachment://green-line.jpg")
        win_embed.add_field(
            name="Score:",
            value=f"{emojis['plus']} {winner_xp}xp:  {winner.mention}\
                \n{emojis['minus']} {loser_xp}xp: {loser.mention} ",
        )

        self.stop()

        await self.message.edit(
            content=None,
            embed=win_embed,
            view=None,
            file=dc.File("bot/assets/green-line.jpg"),
        )

    @ui.button(label="Punch", emoji=emojis["punch"])
    async def punch(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user.id == self.current_player.id:
            return await interaction.response.send_message(
                "It's not your turn.", ephemeral=True
            )

        await interaction.response.defer()

        damage = randint(5, 25)

        has_lost = await self.damage(self.next_player, damage)

        if has_lost:
            return await self.end(self.current_player, self.next_player)

        self.action = f"{self.current_player.display_name} punched {self.next_player.display_name} dealing {damage} damage!"

        self.swap()
        await self.update()

    @ui.button(label="Snowball Attack", emoji=emojis["snowball"])
    async def snowball(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user.id == self.current_player.id:
            return await interaction.response.send_message(
                "It's not your turn.", ephemeral=True
            )

        await interaction.response.defer()

        dmg = randint(6, 30)
        choices = [dmg, dmg, 0, dmg, dmg]

        damage = choice(choices)

        self.action = f"{self.current_player.display_name} threw a snowball on {self.next_player.display_name} dealing {damage} damage!"

        if damage == 0:
            self.action = f"{self.current_player.display_name} tried to throw snowball but his aim sucks!"

        has_lost = await self.damage(self.next_player, damage)

        if has_lost:
            return await self.end(self.current_player, self.next_player)

        self.swap()
        await self.update()

    @ui.button(
        label="Upgrade Defense", style=dc.ButtonStyle.primary, emoji=emojis["shield"]
    )
    async def defend(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user.id == self.current_player.id:
            return await interaction.response.send_message(
                "It's not your turn.", ephemeral=True
            )

        if self.stats[self.current_player]["shield"] == 100:
            return await interaction.response.send_message(
                "Your shield is maxed out. try something else", ephemeral=True
            )

        await interaction.response.defer()

        upgrade = randint(5, 25)
        self.stats[self.current_player]["shield"] += upgrade

        if self.stats[self.current_player]["shield"] > 100:
            self.stats[self.current_player]["shield"] = 100

        self.action = f"{self.current_player.display_name} upgraded their defense!"
        self.swap()
        await self.update()


class DuelInvite(ui.View):
    def __init__(self, player: dc.Member, author: dc.Member, bot):
        super().__init__(timeout=90)

        self.bot = bot
        self.author = author
        self.player = player

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

        await self.message.edit(
            embed=dc.Embed(title="Duel timed out.", color=0x2F3136), view=self
        )

    @ui.button(label="Accept", style=dc.ButtonStyle.success)
    async def accept(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user.id == self.player.id:
            return await interaction.response.send_message(
                "This is not for you.", ephemeral=True
            )
        self.disable_all_items()
        self.stop()

        await self.start_duel(interaction)

    @ui.button(label="Reject", style=dc.ButtonStyle.danger)
    async def reject(self, button: ui.Button, interaction: dc.Interaction):
        if not interaction.user.id == self.player.id:
            return await interaction.response.send_message(
                "This is not for you.", ephemeral=True
            )
        self.disable_all_items()
        self.stop()

        reject_embed = dc.Embed(title="Duel rejected.", color=0x2F3136)
        await interaction.response.edit_message(embed=reject_embed, view=self)

    async def start_duel(self, inter: dc.Interaction):
        """Sends the game message and prevents multiple game sessions"""
        playing = []

        if inter.user.id in self.bot.on_going_duels:
            playing.append("You")

        if self.author.id in self.bot.on_going_duels:
            playing.append(self.author.mention)

        if playing:
            players = " and ".join(playing)
            return await inter.response.send_message(
                f"{players} already have an ongoing `duel` game...", ephemeral=True
            )

        self.bot.on_going_duels.extend([self.author.id, inter.user.id])

        view = Duel(players=[self.author, self.player], bot=self.bot)

        await inter.response.send_message(
            f"{view.current_player.mention}, It's your turn.",
            embed=view.game_embed,
            view=view,
        )


class DuelCommand(dc.Cog):
    def __init__(self, bot):
        self.bot = bot

    @dc.command(name="duel")
    @dc.option("player", dc.Member, description="Your best friend")
    @cmds.cooldown(1, 5, cmds.BucketType.member)
    async def duel_cmd(self, ctx: dc.ApplicationContext, player: dc.Member):
        """Play a 1v1 battle!"""
        if ctx.author == player or player.bot:
            return await ctx.respond(
                "You can't play with yourself or with a bot...", ephemeral=True
            )
        invite_embed = dc.Embed(
            title="Do you accept challenge?",
            description=f"{ctx.author.mention} invited you to a duel!",
            color=0x2F3136,
        )
        invite_embed.set_footer(text="you have 60s to respond.")

        duel = DuelInvite(player=player, author=ctx.author, bot=self.bot)

        await ctx.respond(player.mention, embed=invite_embed, view=duel)


def setup(bot: _Bot):
    bot.add_cog(DuelCommand(bot))
