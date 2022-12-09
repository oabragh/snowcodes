import typing as t
from random import choice

from discord import Member
from discord.ui import View


class TicTacToe(View):
    def __init__(self, players: t.List[Member], bot):
        super().__init__(timeout=30, disable_on_timeout=True)
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

        self.players = [{players[0]: "X"}, {players[1]: "O"}]
        self.current_player = choice(players)
