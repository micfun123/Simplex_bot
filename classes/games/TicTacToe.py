from classes.Game import Game
from classes.Player import Player
from time import time
import random


class TicTacToePlayer(Player):

    def __init__(self, discord_id: int, symbol: str):
        super().__init__(discord_id)
        self.symbol = symbol
        self.emoji = self.get_emoji()
        self.proposed_tie = False

    def get_emoji(self) -> str:

        if self.symbol == "x":

            return "❌"

        else:

            return "🟢"


class TicTacToeBoard:

    def __init__(self):
        self.board = ["."] * 9

    def check_win(self, symbol: str) -> bool:
        # horizontal checks

        for i in range(0, 9, 3):

            if self.board[i:i+3] == [symbol] * 3:

                return True

        # vertical checks
        for i in range(2):

            if self.board[i::3] == [symbol] * 3:

                return True

        # diagonal checks
        if self.board[0::4] == [symbol] * 3:

            return True

        elif [self.board[2], self.board[4], self.board[8]] == [symbol] * 3:

            return True

        return False

    def place(self, symbol: str, pos: int) -> bool:

        if self.board[pos] == ".":

            self.board[pos] = symbol

            return True

        return False

    def display(self) -> str:

        number_to_emoji: dict[str, str] = {
            "0": ":zero:", "1": ":one:", "2": ":two:", "3": ":three:", "4": ":four:",
            "5": ":five:", "6": ":six:", "7": ":seven:", "8": ":eight:", "9": ":nine:"
        }

        txt = ""

        for row in range(3):

            for column in range(3):

                pos = row * 3 + column

                if self.board[pos] == "o":

                    txt += "🟢"

                elif self.board[pos] == "x":

                    txt += "❌"

                else:

                    txt += number_to_emoji[str(pos)]

            txt += "\n"

        return txt


class TicTacToeGame(Game):

    TIMEOUT = 100  # if you change this make sure to change it in the tchallenge command to

    def __init__(self, player_ids: list[int]):
        super().__init__("TicTacToe", 2, 2)

        self.player_ids: list[int] = player_ids
        self.players: list[TicTacToePlayer] = self.construct_players()
        self.current_round_player: TicTacToePlayer = self.players[0]

        self.board = TicTacToeBoard()
        self.ongoing = False
        self.timer = 0

    def construct_players(self):

        symbol = "o"

        random.shuffle(self.player_ids)

        players = []

        for player_id in self.player_ids:  # 2 iterations

            players.append(TicTacToePlayer(player_id, symbol))
            symbol = "x"

        return players

    def next_player(self):
        return self.players[0] if self.players[0] != self.current_round_player else self.players[1]

    def next_round(self):
        self.timer = time()
        self.current_round_player = self.next_player()

    def get_player_by_id(self, discord_id: int):
        return self.players[0] if self.players[0].discord_id == discord_id else self.players[1]
