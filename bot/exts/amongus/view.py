from discord import Colour, Embed, User
from discord.ui import View

from bot.constants import emojis


class Amongus(View):

    _score = 0
    _win_bonus = 0  # you get this when you when, default to 0

    def __init__(self, *, player: User, bot, impostors: int):
        super().__init__(timeout=30, disable_on_timeout=True)

        self.helper = bot.dbh
        self.player = player
        self.impostors = impostors
        self.msg = (
            "Click on crewmates (if you pick an impostor you lose...)\n"
            f"Current score: {self.score} ({self.reward} {emojis['currency']})"
        )

    async def lost(self):
        """Called when pressing an impostor button"""

        await self.helper.update_user_wallet(self.player.id, self.reward)

        lose_embed = Embed(title="You lost!", colour=Colour.red())
        lose_embed.add_field(name="Score", value=self.score)
        lose_embed.add_field(name="Reward", value=f"{self.reward} {emojis['currency']}")

        self.disable_all_items()
        self.stop()

        await self.message.edit(content=None, embed=lose_embed, view=None)

    async def update(self):
        """Update the message with the current score"""
        self.score += 1

        if self.score == 10 - self.impostors:  # If every crewmate button is clicked
            self._win_bonus = 50000

            await self.helper.update_user_wallet(self.player.id, self.reward)

            win_embed = Embed(title="You won!", colour=Colour.green())
            win_embed.add_field(name="Score", value=self.score)
            win_embed.add_field(
                name="Reward", value=f"{self.reward} {emojis['currency']}"
            )

            return await self.message.edit(content=None, embed=win_embed, view=None)

        await self.message.edit(content=self.msg, view=self)

    @property
    def score(self) -> int:
        """the current score state"""
        return self._score

    @score.setter
    def score(self, num: int) -> None:
        """update the score state"""

        self._score += 1
        self.msg = (
            "Click on crewmates (if you pick an impostor you lose...)\n"
            f"Current score: {num} ({self.reward} {emojis['currency']})"
        )

    @property
    def reward(self) -> int:
        """Returns the reward depending on the current score"""
        result = self.score * (self.impostors * 1750) + self._win_bonus

        if self.score == 0:
            result += 500

        return result
