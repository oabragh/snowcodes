from random import randint

from discord import Colour, Embed, User, File
from discord.ui import View

from bot.constants import emojis


class Bigrat(View):
    def __init__(self, *, player: User, bot):
        super().__init__(timeout=30, disable_on_timeout=True)

        self.helper = bot.dbh
        self.player = player


    async def lost(self):
        """Called when the player chose the wrong button"""

        chance = randint(1, 5)

        bigrat_img = File("bot/assets/bigrat.png")

        lose_embed = Embed(title="You lost!", colour=Colour.red())
        lose_embed.set_image(url="attachment://bigrat.png")

        if chance == 3:
            reward = randint(1000, 2500)

            lose_embed.description = f"Oh, Bigrat gave you {reward} {emojis['currency']} for playing with him!"
            await self.helper.update_user_wallet(self.player.id, reward)

        self.disable_all_items()
        self.stop()

        await self.message.edit(embed=lose_embed, view=self, file=bigrat_img)

    async def won(self):
        """Called when the player clicks the right button"""
        reward = randint(20000, 25000)
        reward_msg = f"You got {reward} {emojis['currency']} from bigrat!"

        await self.helper.update_user_wallet(self.player.id, reward)

        hat_bigrat_img = File("bot/assets/bigrat-christmas-hat.png")

        win_embed = Embed(
            title="You won!", colour=Colour.green(), description=reward_msg
        )
        win_embed.set_image(url="attachment://bigrat-christmas-hat.png")

        self.disable_all_items()
        self.stop()

        return await self.message.edit(
            embed=win_embed, view=self, file=hat_bigrat_img
        )
