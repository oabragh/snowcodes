import discord as dc


class Database(dc.Cog):
    """Helper functions for querying the database"""

    def __init__(self, bot):
        self.bot = bot

    async def create_user(self, id: int, score: int = 0):
        """Add player to database"""
        async with self.bot.conn.cursor() as cur:
            query = "INSERT INTO players (id, score) VALUES (?, ?)"
            await cur.execute(query, (id, score))
            await self.bot.conn.commit()

        return (str(id), score)

    async def get_user_stats(self, id: int):
        """Get player stats"""
        async with self.bot.conn.cursor() as cur:
            query = "SELECT * FROM players WHERE id=?"
            await cur.execute(query, (id,))
            result = await cur.fetchone()

            if not result:
                result = await self.create_user(id)

        return result

    async def get_all_stats(self):
        async with self.bot.conn.cursor() as cur:
            query = "SELECT * FROM players"
            await cur.execute(query)

            result = await cur.fetchall()

        return result

    async def update_user_score(self, id: int, change: int):
        """Update player score"""
        async with self.bot.conn.cursor() as cur:
            id, score = await self.get_user_stats(id)
            query = "UPDATE players SET score=? WHERE id=?"
            score += change

            if score <= 0:  # Score can't be negative
                score = 0

            await cur.execute(query, (score, id))
            await self.bot.conn.commit()

        return (id, score)


def setup(bot):
    bot.add_cog(Database(bot))
