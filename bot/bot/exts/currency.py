from discord import ApplicationContext, slash_command, Member, Embed, option, Colour
from discord.ext.commands import Cog

from bot.bot import _Bot

from bot.constants import emojis


class Currency(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="balance", guild_ids=[1041363391790465075])
    @option("player", Member)
    async def balance_cmd(self, ctx: ApplicationContext, player: Member = None):
        """Show your or someone else's balance."""

        player = player or ctx.author

        if player.bot:
            return await ctx.respond(
                "Bots can't play D: ||(01110011 01101111 01110010 01110010 01111001)||"
            )

        # Placeholders until i add a database :)
        player_wallet = 000
        player_bank = 000
        player_rank = 000

        desc = (
            f"> Wallet: {player_wallet} {emojis['currency']}\n"
            f"> Vault: {player_bank} {emojis['currency']}"
        )

        bal_embed = Embed(
            title=f"{player.display_name}'s Balance:", description=desc, colour=0x2F3136
        )

        bal_embed.set_footer(text=f"Rank #{player_rank} globally.")

        await ctx.respond(embed=bal_embed)

    @slash_command(name="pay", guild_ids=[1041363391790465075])
    @option("player", Member, description="Your best friend's name :)")
    @option("amount", int, description="Amount of candies to send!")
    async def pay_cmd(self, ctx: ApplicationContext, player: Member, amount: int):
        """Send money from your wallet!"""

        if amount <= 0:
            return await ctx.respond("Too low!", ephemeral=True)

        if player == ctx.author or player.bot:
            return await ctx.respond(
                "Hey, you can't money to yourself or bots, send to a real friend!",
                ephemeral=True,
            )

        your_wallet = 0
        target_wallet = 0

        transaction_embed = Embed(
            title="Successfully sent!",
            description=f"-{amount} {emojis['currency']}",
            colour=Colour.blue(),
        )
        transaction_embed.add_field(
            name="Your wallet", value=f"{your_wallet} {emojis['currency']}"
        )
        transaction_embed.add_field(
            name=f"{player.display_name}'s wallet",
            value=f"{target_wallet} {emojis['currency']}",
        )

        await ctx.respond(embed=transaction_embed)


def setup(bot: _Bot):
    bot.add_cog(Currency(bot))
