class DBHelpers:
    """Helper functions for querying the database"""

    def __init__(self, bot):
        self.bot = bot

    async def create_user(self, id: int, wallet: int = 0):
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
                result = await self.create_user(id)

            await self.bot.conn.commit()

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
