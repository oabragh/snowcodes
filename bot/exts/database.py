from discord import Cog

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

    async def update_user_wallet(self, id: int, increment: int):
        """Update player wallet"""
        async with self.bot.conn.cursor() as cur:
            id, wallet, vault, max = await self.get_user_balance(id)
            query = "UPDATE balances SET wallet=? WHERE id=?"
            wallet += increment

            await cur.execute(query, (wallet, id))
            await self.bot.conn.commit()

        return (id, wallet, vault, max)
    

    async def create_user_inventory(self, id: int, item = None):
        async with self.bot.conn.cursor() as cur:
            query = "INSERT INTO inventory (id) VALUES (?)"
            await cur.execute(query, (id,))
            await self.bot.conn.commit()
        
        return (id,)

    async def get_user_inventory(self, id: int):
        """Returns the user items"""
        async with self.bot.conn.cursor() as cur:
            query = "SELECT * FROM inventory WHERE id=?"
            await cur.execute(query, (id,))
            result = await cur.fetchone()

            if not result:
                result = await self.create_user_inventory(id)

            await self.bot.conn.commit()

        return result

    
    async def update_user_item(self, user_id: int, item, ):
        """Adds an item to user"""
        async with self.bot.conn.cursor as cur:
            await add_user(user_id)

def setup(bot):
    bot.add_cog(Database(bot))