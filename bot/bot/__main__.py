"""
MIT License (read LICENSE for details)

Copyright (c) 2022 oabragh
"""

from bot.bot import _Bot
from os import getenv


def main():
    """Bot entrypoint."""

    bot = _Bot()

    bot.load_extensions_from_module("bot.exts")

    bot.run(getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
