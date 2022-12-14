"""discord.Bot subclass file"""

import aiosqlite
from discord import Bot, Cog


class _Bot(Bot):
    def __init__(self):
        super().__init__()

        self.conn: aiosqlite.Connection = None

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        if not self.conn:
            self.conn = await aiosqlite.connect("./bot/database.db")

        return await super().start(token, reconnect=reconnect)

    async def close(self) -> None:
        if self.conn:
            await self.conn.close()

        return await super().close()

    async def on_ready(self) -> None:
        await self.setup_database()

    async def setup_database(self) -> None:
        queries = [
            """
            CREATE TABLE IF NOT EXISTS "players" (
                "id"	    TEXT    NOT NULL UNIQUE,
                "score"	    INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY("id")
            );
            """
        ]

        async with self.conn.cursor() as cur:
            for i in queries:
                await cur.execute(i)
            await self.conn.commit()

    @property
    def db(self) -> Cog:
        return self.get_cog("Database")
