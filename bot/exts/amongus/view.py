from discord import Embed, User
from discord.ui import View

from bot.constants import emojis


class Amongus(View):

    _score = 0
    _win_bonus = 0  # you get this when you win, default to 0

    def __init__(self, *, player: User, bot, impostors: int):
        super().__init__(timeout=30, disable_on_timeout=True)

        self.bot = bot
        self.player = player
        self.impostors = impostors

    async def lost(self):
        """Called when pressing an impostor button"""

        await self.bot.db.update_user_wallet(self.player.id, self.reward)

        lose_embed = Embed(title="You lost!", color=0x2F3136)
        lose_embed.add_field(name="Score", value=self._score)
        lose_embed.add_field(
            name="Reward", value=f"{self.reward} {emojis['currency']}")
        lose_embed.add_field(name="Impostors", value=" ".join(  # value = every impostor button's emoji
            [str(b.emoji) for b in self.children if b.impostor]))

        self.disable_all_items()
        self.stop()

        await self.message.edit(content=None, embed=lose_embed, view=None)

    async def update(self):
        """Update the message with the current score"""
        self._score += 1

        if self._score == 10 - self.impostors:  # If every crewmate button is clicked
            self._win_bonus = 50000

            await self.bot.db.update_user_wallet(self.player.id, self.reward)

            win_embed = Embed(title="You won!", color=0x2F3136)
            win_embed.add_field(name="Score", value=self._score)
            win_embed.add_field(
                name="Reward", value=f"{self.reward} {emojis['currency']}")

            return await self.message.edit(content=None, embed=win_embed, view=None)

        await self.message.edit(content=self.msg, view=self)

    @property
    def msg(self) -> int:
        """the current score state"""
        return ("Click on crewmates (if you pick an impostor you lose...)\n"
                f"Current score: {self._score} ({self.reward} {emojis['currency']})")

    @property
    def reward(self) -> int:
        """Returns the reward depending on the current score"""
        result = self._score * (self.impostors * 750) + self._win_bonus

        if self._score == 0:
            result += 250

        return result
