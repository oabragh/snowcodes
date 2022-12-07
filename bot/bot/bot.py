"""commands.Bot subclass file"""

from discord import Bot
import aiohttp

class _Bot(Bot):
    def __init__(self):
        super().__init__()

        self.session: aiohttp.ClientSession = None
    
    async def start(self, token: str, *, reconnect: bool = True) -> None:
        async with aiohttp.ClientSession() as self.session:
            return await super().start(token, reconnect=reconnect)