from discord import Cog

from bot.errors import (InvalidAmount, NotEnoughVault, NotEnoughVaultCapacity,
                        NotEnoughWallet, VaultEmpty, WalletEmpty)


class Database(Cog):
    """Helper functions for querying the database"""

    def __init__(self, bot):
        self.bot = bot

    async def create_user_wallet(self, id: int, wallet: int = 0):
        """Add player to database"""
        async with self.bot.conn.cursor() as cur:
            query = "INSERT INTO balances (id, wallet) VALUES (?, ?)"
            await cur.execute(query, (id, wallet))
            await self.bot.conn.commit()

        return (id, wallet, 0, 25000)

    async def get_user_balance(self, id: int):
        """Get player balance"""
        async with self.bot.conn.cursor() as cur:
            query = "SELECT * FROM balances WHERE id=?"
            await cur.execute(query, (id,))
            result = await cur.fetchone()

            if not result:
                result = await self.create_user_wallet(id)

        return result

    async def update_user_wallet(self, id: int, change: int):
        """Update player wallet"""
        async with self.bot.conn.cursor() as cur:
            id, wallet, vault, max = await self.get_user_balance(id)
            query = "UPDATE balances SET wallet=? WHERE id=?"
            wallet += change

            await cur.execute(query, (wallet, id))
            await self.bot.conn.commit()

        return (id, wallet, vault, max)

    async def update_user_vault(self, id: int, change: int):
        """Update player wallet"""
        async with self.bot.conn.cursor() as cur:
            id, wallet, vault, max = await self.get_user_balance(id)
            query = "UPDATE balances SET vault=? WHERE id=?"
            wallet += change

            await cur.execute(query, (wallet, id))
            await self.bot.conn.commit()

        return (id, wallet, vault, max)

    # async def deposit_user_wallet(self, id: int, amount: int | str):
    #     id, wallet, vault, max = await self.get_user_balance(id)

    #     if not amount in ["all", "max"] and not amount.isdigit():
    #         raise InvalidAmount()

    #     if amount.lower() == "all":
    #         amount = wallet
    #     elif amount.lower() == "max":
    #         amount = max-vault
            
    #     amount = int(amount)

    #     if wallet == 0:
    #         raise WalletEmpty()

    #     elif wallet > amount:
    #         raise NotEnoughWallet()

    #     elif (vault + amount) > max:
    #         raise NotEnoughVaultCapacity()

    #         query = "UPDATE balances SET vault=?, wallet=? WHERE id=?"
    #         vault += amount
    #         wallet -= amount

    #         await cur.execute(query, (vault, wallet, id))
    #         await self.bot.conn.commit()

    #     return (id, wallet, vault, max)

    # async def withdraw_user_vault(self, id: int, amount: int | str):
    #     async with self.bot.conn.cursor() as cur:
    #         id, wallet, vault, max = await self.get_user_balance(id)

    #         if not amount in ["all", "max"] and not amount.isdigit():
    #             raise InvalidAmount()

    #         if amount == "all":
    #             amount = vault
    #         if str(amount).isdigit():
    #             amount = int(amount)

    #         if vault == 0:
    #             raise VaultEmpty()

    #         if vault < amount:
    #             raise NotEnoughVault()

    #         query = "UPDATE balances SET vault=?, wallet=? WHERE id=?"
    #         vault -= amount
    #         wallet += amount

    #         await cur.execute(query, (vault, wallet, id))
    #         await self.bot.conn.commit()

    #     return (id, wallet, vault, max)

    # async def create_user_inventory(self, id: int, item = None):
    #     async with self.bot.conn.cursor() as cur:
    #         query = "INSERT INTO inventory (id) VALUES (?)"
    #         await cur.execute(query, (id,))
    #         await self.bot.conn.commit()

    #     return (id,)

    # async def get_user_inventory(self, id: int):
    #     """Returns the user items"""
    #     async with self.bot.conn.cursor() as cur:
    #         query = "SELECT * FROM inventory WHERE id=?"
    #         await cur.execute(query, (id,))
    #         result = await cur.fetchone()

    #         if not result:
    #             result = await self.create_user_inventory(id)

    #         await self.bot.conn.commit()

    #     return result

    # async def update_user_item(self, user_id: int, item, ):
    #     """Adds an item to user"""
    #     async with self.bot.conn.cursor as cur:
    #         await add_user(user_id)


def setup(bot):
    bot.add_cog(Database(bot))
