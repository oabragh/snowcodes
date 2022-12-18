"""discord.Bot subclass file"""

import aiosqlite
import discord as dc
import discord.ext.commands as cmds


class _Bot(dc.Bot):
    def __init__(self):
        intents = dc.Intents.default()
        intents.members = True
        activity = dc.Activity(type=dc.ActivityType.watching, name="You")

        super().__init__(intents=intents, activity=activity)

        self.conn: aiosqlite.Connection = None
        self.on_going_duels: list = []
        self.on_going_amongus: list = []
        self.on_going_bigrat: list = []
        self.on_going_rps: list = []

    async def on_application_command_error(
        self, ctx: dc.ApplicationContext, exception: dc.DiscordException
    ):
        if ctx.command.has_error_handler():
            return

        if isinstance(exception, cmds.CommandOnCooldown):
            await ctx.respond("Please don't spam bot commands!", ephemeral=True)

        else:
            await ctx.respond(
                "Some error occured! please try again later", ephemeral=True
            )

            raise exception

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
        self.get_user

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
    def db(self) -> dc.Cog:
        return self.get_cog("Database")
