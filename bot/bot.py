"""commands.Bot subclass file"""

from discord import Bot, Interaction
import aiosqlite


class _Bot(Bot):
    def __init__(self):
        super().__init__()

        self.conn: aiosqlite.Connection = None

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        async with aiosqlite.connect("./bot/database.db") as self.conn:
            return await super().start(token, reconnect=reconnect)

    async def on_ready(self) -> None:
        await self.setup_database()

    async def setup_database(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS "balances" (
                "id"	TEXT NOT NULL UNIQUE,
                "wallet"	INTEGER NOT NULL DEFAULT 1000,
                "vault"	INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY("id")
            );
        """
        await self.conn.execute(query)
        await self.conn.commit()
