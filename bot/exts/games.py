from discord import ApplicationContext, slash_command, option, ButtonStyle, Interaction
from discord.ui import View, Button
from discord.ext.commands import Cog

from bot.bot import _Bot
from random import randint


class AmongieButton(Button):
    def __init__(self, impostor=False):
        super().__init__(style=ButtonStyle.gray, emoji="🙍‍♂️")

        self.impostor = impostor

    async def callback(self, interaction: Interaction):
        if self.impostor:
            await interaction.message.edit(content="You lost!", view=None)

        else:
            self.style = ButtonStyle.success
            self.disabled = True
            self.view.score += 1

            await interaction.
            await interaction.message.edit("Click on crewmates (if you pick an impostor you lose...)\n"
                                           f"Current score: {self.view.score}", view=self.view)

        return await super().callback(interaction)


class Games(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="among-us", guild_ids=[1041363391790465075])
    @option(
        "impostors",
        description="Higher is harder but you get more rewards",
        choices=["3", "4", "5"],
    )
    async def amogus_cmd(self, ctx: ApplicationContext, impostors: int):

        view = View(timeout=30, disable_on_timeout=True)
        view.score = 0

        buttons = [AmongieButton() for _ in range(10)]
        impostor_ids = []

        for _ in range(impostors):
            rand = randint(0, 9)

            while rand in impostor_ids:
                rand = randint(0, 9)

            impostor_ids.append(rand)
            print(rand)
            buttons[rand].impostor = True

        for i in buttons:
            print(i.impostor)
            view.add_item(i)

        await ctx.respond(
            "Click on crewmates (if you pick an impostor you lose...)\n"
            f"Current score: {view.score}", view=view)


def setup(bot: _Bot):
    bot.add_cog(Games(bot))
