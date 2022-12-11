from discord import (ApplicationCommandError, ApplicationContext, Cog, Embed,
                     File, Member, command, option)

from bot.bot import _Bot
from bot.constants import emojis
from bot.errors import (InvalidAmount, NotEnoughVault, NotEnoughVaultCapacity,
                        NotEnoughWallet, VaultEmpty, WalletEmpty)


class Currency(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="balance", guild_ids=[1041363391790465075])
    @option("player", Member)
    async def balance_cmd(self, ctx: ApplicationContext, player: Member = None):
        """Show your or someone else's balance."""

        player = player or ctx.author

        if player.bot:
            return await ctx.respond(
                "Bots can't play D: ||(01110011 01101111 01110010 01110010 01111001)||",
                ephemeral=True,
            )

        data = await self.bot.db.get_user_balance(player.id)

        player_wallet = data[1]
        player_vault = data[2]
        player_max_vault = data[3]

        balance_embed = Embed(
            title=f"{player.display_name}'s Balance:",
            color=0x2F3136,
            description=(
                f"Wallet: {player_wallet} {emojis['currency']}\n"
                f"Vault: {player_vault}/{player_max_vault} {emojis['currency']}"
            ),
        )
        balance_embed.set_thumbnail(url="attachment://balance.png")
        balance_png = File("bot/assets/balance.png")
        await ctx.respond(embed=balance_embed, file=balance_png)

    @command(name="pay", guild_ids=[1041363391790465075])
    @option("player", Member, description="Your best friend's name :)")
    @option("amount", int, description="Amount of coins to send!")
    async def pay_cmd(self, ctx: ApplicationContext, player: Member, amount: int):
        """Send money from your wallet!"""

        if amount <= 0:
            return await ctx.respond("Too low!", ephemeral=True)

        if player == ctx.author or player.bot:
            return await ctx.respond(
                "Hey, you can't money to yourself or bots, send to a real friend!",
                ephemeral=True,
            )

        your_bal = await self.bot.db.get_user_balance(ctx.author.id)

        if your_bal[1] < amount:
            return await ctx.respond(
                "Whoops! you don't have that amount.",
                ephemeral=True,
            )

        _, your_wallet, _, _ = await self.bot.db.update_user_wallet(ctx.author.id, -amount)
        _, target_wallet, _, _ = await self.bot.db.update_user_wallet(player.id, amount)

        transaction_embed = Embed(
            title="Successfully sent!",
            description=f"-{amount} {emojis['currency']}",
            color=0x2F3136
        )
        transaction_embed.add_field(
            name="Your wallet", value=f"{your_wallet} {emojis['currency']}"
        )
        transaction_embed.add_field(
            name=f"{player.display_name}'s wallet",
            value=f"{target_wallet} {emojis['currency']}",
        )

        await ctx.respond(embed=transaction_embed)

    @command(name="deposit", guild_ids=[1041363391790465075])
    @option("amount", str)
    async def deposit_cmd(self, ctx: ApplicationContext, amount: str):
        """Deposit money to your vault"""
        if amount.isdigit() and int(amount) <= 0:
            return await ctx.respond("Too low!", ephemeral=True)

        try:
            _, wallet, vault, _ = await self.bot.db.deposit_user_wallet(ctx.author.id, amount)
            success_embed = Embed(title="You deposited", color=0x2F3136)
            success_embed.add_field(
                name="Wallet now:", value=f"{wallet} {emojis['currency']}")
            success_embed.add_field(
                name="Vault now:", value=f"{vault} {emojis['currency']}")

            await ctx.respond(embed=success_embed)

        except ApplicationCommandError as e:
            if isinstance(e, NotEnoughVaultCapacity):
                await ctx.respond("Your vault capacity is small. Use `Vault Upgrade Token` to upgrade it", ephemeral=True)

            elif isinstance(e, NotEnoughWallet):
                await ctx.respond("You don't have that amount...", ephemeral=True)

            elif isinstance(e, WalletEmpty):
                await ctx.respond("Your wallet is empty.", ephemeral=True)

            elif isinstance(e, InvalidAmount):
                await ctx.respond("Invalid amount. please enter a valid number")

    @command(name="withdraw", guild_ids=[1041363391790465075])
    @option("amount", str)
    async def withdraw_cmd(self, ctx: ApplicationContext, amount: str):
        """Withdraw money from your vault"""
        if amount.isdigit() and int(amount) <= 0:
            return await ctx.respond("Too low!", ephemeral=True)

        try:
            _, wallet, vault, _ = await self.bot.db.withdraw_user_vault(ctx.author.id, amount)
            success_embed = Embed(title="You withdrew", color=0x2F3136)
            success_embed.add_field(
                name="Wallet now:", value=f"{wallet} {emojis['currency']}")
            success_embed.add_field(
                name="Vault now:", value=f"{vault} {emojis['currency']}")

            await ctx.respond(embed=success_embed)

        except ApplicationCommandError as e:
            if isinstance(e, NotEnoughVault):
                await ctx.respond("You don't have that amount in vault...", ephemeral=True)

            if isinstance(e, VaultEmpty):
                await ctx.respond("Your vault is empty.", ephemeral=True)

            elif isinstance(e, InvalidAmount):
                await ctx.respond("Invalid amount. please enter a valid number")


def setup(bot: _Bot):
    bot.add_cog(Currency(bot))