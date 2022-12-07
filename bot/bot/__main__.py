"""
MIT License (read LICENSE for details)

Copyright (c) 2022 oabragh
"""

from bot.bot import _Bot
from os import getenv, listdir


def main():
    """Bot entrypoint."""

    bot = _Bot()

    exts = ["bot.exts."+i.replace(".py", "")
                        for i in listdir("./bot/exts") if i.endswith(".py")]

    for i in exts:
        bot.load_extension(i)

    bot.run(getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
