"""discord.Bot subclass file"""

import aiosqlite
from discord import Bot

from bot.helpers import DBHelpers


class _Bot(Bot):
    def __init__(self):
        super().__init__()

        self.conn: aiosqlite.Connection = None
        self.dbh = DBHelpers(self)

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
        query = """
            CREATE TABLE IF NOT EXISTS "balances" (
                "id"	    TEXT NOT NULL UNIQUE,
                "wallet"	INTEGER NOT NULL DEFAULT 1000,
                "vault"	    INTEGER NOT NULL DEFAULT 0,
                "max"       INTEGER NOT NULL DEFAULT 25000,
                PRIMARY KEY("id")
            );
        """

        async with self.conn.cursor() as cur:
            await cur.execute(query)
            await self.conn.commit()
