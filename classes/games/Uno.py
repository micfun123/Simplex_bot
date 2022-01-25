from classes.Game import Game
from classes.Player import Player
from discord import User
from time import time
import random


IMAGES: dict[str, str] = {
    "r0": "https://cdn.discordapp.com/attachments/848488501335031870/848508777371926538/Screenshot_223.png",
    "r1": "https://cdn.discordapp.com/attachments/848488501335031870/848488560583245864/Screenshot_213.png",
    "r2": "https://cdn.discordapp.com/attachments/848488501335031870/848508261148917810/Screenshot_215.png",
    "r3": "https://cdn.discordapp.com/attachments/848488501335031870/848508338182160394/Screenshot_216.png",
    "r4": "https://cdn.discordapp.com/attachments/848488501335031870/848508560228089896/Screenshot_217.png",
    "r5": "https://cdn.discordapp.com/attachments/848488501335031870/848508554255532032/Screenshot_218.png",
    "r6": "https://cdn.discordapp.com/attachments/848488501335031870/848508552599175178/Screenshot_219.png",
    "r7": "https://cdn.discordapp.com/attachments/848488501335031870/848508782387658782/Screenshot_220.png",
    "r8": "https://cdn.discordapp.com/attachments/848488501335031870/848508780899598386/Screenshot_221.png",
    "r9": "https://cdn.discordapp.com/attachments/848488501335031870/848508778927095848/Screenshot_222.png",
    "r+2": "https://cdn.discordapp.com/attachments/848488501335031870/848509834881794058/Screenshot_226.png",
    "rx": "https://cdn.discordapp.com/attachments/848488501335031870/848509833133031424/Screenshot_224.png",
    "r<>": "https://cdn.discordapp.com/attachments/848488501335031870/848509831610630164/Screenshot_225.png",

    "g0": "https://cdn.discordapp.com/attachments/848488501335031870/848514966428581888/Screenshot_262.png",
    "g1": "https://cdn.discordapp.com/attachments/848488501335031870/848515042491629568/Screenshot_253.png",
    "g2": "https://cdn.discordapp.com/attachments/848488501335031870/848515039472123944/Screenshot_254.png",
    "g3": "https://cdn.discordapp.com/attachments/848488501335031870/848515037903061023/Screenshot_255.png",
    "g4": "https://cdn.discordapp.com/attachments/848488501335031870/848514977559609344/Screenshot_256.png",
    "g5": "https://cdn.discordapp.com/attachments/848488501335031870/848514975546736650/Screenshot_257.png",
    "g6": "https://cdn.discordapp.com/attachments/848488501335031870/848514973898637322/Screenshot_258.png",
    "g7": "https://cdn.discordapp.com/attachments/848488501335031870/848514971952087040/Screenshot_259.png",
    "g8": "https://cdn.discordapp.com/attachments/848488501335031870/848514970286686238/Screenshot_260.png",
    "g9": "https://cdn.discordapp.com/attachments/848488501335031870/848514968290852885/Screenshot_261.png",
    "g+2": "https://cdn.discordapp.com/attachments/848488501335031870/848514958881718282/Screenshot_265.png",
    "gx": "https://cdn.discordapp.com/attachments/848488501335031870/848514964036648980/Screenshot_263.png",
    "g<>": "https://cdn.discordapp.com/attachments/848488501335031870/848514960752771082/Screenshot_264.png",

    "b0": "https://cdn.discordapp.com/attachments/848488501335031870/848513833911058463/Screenshot_249.png",
    "b1": "https://cdn.discordapp.com/attachments/848488501335031870/848513914119258122/Screenshot_240.png",
    "b2": "https://cdn.discordapp.com/attachments/848488501335031870/848513912264720394/Screenshot_241.png",
    "b3": "https://cdn.discordapp.com/attachments/848488501335031870/848513898247880704/Screenshot_242.png",
    "b4": "https://cdn.discordapp.com/attachments/848488501335031870/848513845438054400/Screenshot_243.png",
    "b5": "https://cdn.discordapp.com/attachments/848488501335031870/848513844992278578/Screenshot_244.png",
    "b6": "https://cdn.discordapp.com/attachments/848488501335031870/848513844682031104/Screenshot_245.png",
    "b7": "https://cdn.discordapp.com/attachments/848488501335031870/848513844812447744/Screenshot_246.png",
    "b8": "https://cdn.discordapp.com/attachments/848488501335031870/848513844581761084/Screenshot_247.png",
    "b9": "https://cdn.discordapp.com/attachments/848488501335031870/848513838533574656/Screenshot_248.png",
    "b+2": "https://cdn.discordapp.com/attachments/848488501335031870/848513829536268318/Screenshot_252.png",
    "bx": "https://cdn.discordapp.com/attachments/848488501335031870/848513832862744586/Screenshot_250.png",
    "b<>": "https://cdn.discordapp.com/attachments/848488501335031870/848513831013318656/Screenshot_251.png",

    "y0": "https://cdn.discordapp.com/attachments/848488501335031870/848512267116347412/Screenshot_236.png",
    "y1": "https://cdn.discordapp.com/attachments/848488501335031870/848511727129460736/Screenshot_227.png",
    "y2": "https://cdn.discordapp.com/attachments/848488501335031870/848511726265040896/Screenshot_228.png",
    "y3": "https://cdn.discordapp.com/attachments/848488501335031870/848511725124059166/Screenshot_229.png",
    "y4": "https://cdn.discordapp.com/attachments/848488501335031870/848511723929600050/Screenshot_230.png",
    "y5": "https://cdn.discordapp.com/attachments/848488501335031870/848511722637492274/Screenshot_231.png",
    "y6": "https://cdn.discordapp.com/attachments/848488501335031870/848512272698834984/Screenshot_232.png",
    "y7": "https://cdn.discordapp.com/attachments/848488501335031870/848512271331491860/Screenshot_233.png",
    "y8": "https://cdn.discordapp.com/attachments/848488501335031870/848512270219870218/Screenshot_234.png",
    "y9": "https://cdn.discordapp.com/attachments/848488501335031870/848512268605325352/Screenshot_235.png",
    "y+2": "https://cdn.discordapp.com/attachments/848488501335031870/848512599585980426/Screenshot_239.png",
    "yx": "https://cdn.discordapp.com/attachments/848488501335031870/848512602426572800/Screenshot_237.png",
    "y<>": "https://cdn.discordapp.com/attachments/848488501335031870/848512601201311814/Screenshot_238.png",

    "+4": "https://cdn.discordapp.com/attachments/848488501335031870/848515484596961330/Screenshot_267.png",
    "cc": "https://cdn.discordapp.com/attachments/848488501335031870/848515488030916658/Screenshot_266.png",

    "gcc": "https://cdn.discordapp.com/attachments/848488501335031870/848515488030916658/Screenshot_266.png",
    "bcc": "https://cdn.discordapp.com/attachments/848488501335031870/848515488030916658/Screenshot_266.png",
    "rcc": "https://cdn.discordapp.com/attachments/848488501335031870/848515488030916658/Screenshot_266.png",
    "ycc": "https://cdn.discordapp.com/attachments/848488501335031870/848515488030916658/Screenshot_266.png",
    "g+4": "https://cdn.discordapp.com/attachments/848488501335031870/848515484596961330/Screenshot_267.png",
    "b+4": "https://cdn.discordapp.com/attachments/848488501335031870/848515484596961330/Screenshot_267.png",
    "r+4": "https://cdn.discordapp.com/attachments/848488501335031870/848515484596961330/Screenshot_267.png",
    "y+4": "https://cdn.discordapp.com/attachments/848488501335031870/848515484596961330/Screenshot_267.png"
}


class UnoCard:

    def __init__(self, name: str, color: str, number: int, special=False, symbol=""):
        self.name = name
        self.color = color  # red, green, blue, yellow, black
        self.number = number  # 0-9, -1 for non numbered colored cards and -2/-3 for wildcards, -4 for color change cards
        self.image = IMAGES[name]
        self.special = special  # +2, reverse, skip turn cards and wild cards

        if symbol == "":
            self.symbol = number

        else:
            self.symbol = symbol  # for display reasons (Ex -> Red X)

    def display(self) -> str:

        if self.color != "black":

            if self.number != -4:

                return f"{self.color.capitalize()} {self.symbol}"

            else:

                return self.color.capitalize()

        else:

            if self.number == -2:
                return "+4 Card"

            else:
                return "Colour Change"


all_cards: dict[str, UnoCard] = {
    "r0": UnoCard("r0", "red", 0), "r1": UnoCard("r1", "red", 1), "r2": UnoCard("r2", "red", 2),
    "r3": UnoCard("r3", "red", 3), "r4": UnoCard("r4", "red", 4), "r5": UnoCard("r5", "red", 5),
    "r6": UnoCard("r6", "red", 6), "r7": UnoCard("r7", "red", 7), "r8": UnoCard("r8", "red", 8),
    "r9": UnoCard("r9", "red", 9), "r+2": UnoCard("r+2", "red", -1, True, "+2"),
    "r<>": UnoCard("r<>", "red", -1, True, "<>"), "rx": UnoCard("rx", "red", -1, True, "X"),
    "g0": UnoCard("g0", "green", 0), "g1": UnoCard("g1", "green", 1), "g2": UnoCard("g2", "green", 2),
    "g3": UnoCard("g3", "green", 3), "g4": UnoCard("g4", "green", 4), "g5": UnoCard("g5", "green", 5),
    "g6": UnoCard("g6", "green", 6), "g7": UnoCard("g7", "green", 7), "g8": UnoCard("g8", "green", 8),
    "g9": UnoCard("g9", "green", 9), "g+2": UnoCard("g+2", "green", -1, True, "+2"),
    "g<>": UnoCard("g<>", "green", -1, True, "<>"), "gx": UnoCard("gx", "green", -1, True, "X"),
    "b0": UnoCard("b0", "blue", 0), "b1": UnoCard("b1", "blue", 1), "b2": UnoCard("b2", "blue", 2),
    "b3": UnoCard("b3", "blue", 3), "b4": UnoCard("b4", "blue", 4), "b5": UnoCard("b6", "blue", 5),
    "b6": UnoCard("b6", "blue", 6), "b7": UnoCard("b7", "blue", 7), "b8": UnoCard("b8", "blue", 8),
    "b9": UnoCard("b9", "blue", 9), "b+2": UnoCard("b+2", "blue", -1, True, "+2"),
    "b<>": UnoCard("b<>", "blue", -1, True, "<>"), "bx": UnoCard("bx", "blue", -1, True, "X"),
    "y0": UnoCard("y0", "yellow", 0), "y1": UnoCard("y1", "yellow", 1), "y2": UnoCard("y2", "yellow", 2),
    "y3": UnoCard("y3", "yellow", 3), "y4": UnoCard("y4", "yellow", 4), "y5": UnoCard("y5", "yellow", 5),
    "y6": UnoCard("y6", "yellow", 6), "y7": UnoCard("y7", "yellow", 7), "y8": UnoCard("y8", "yellow", 8),
    "y9": UnoCard("y9", "yellow", 9), "y+2": UnoCard("y+2", "yellow", -1, True, "+2"),
    "y<>": UnoCard("y<>", "yellow", -1, True, "<>"), "yx": UnoCard("y<>", "yellow", -1, True, "X"),
    "+4": UnoCard("+4", "black", -2, True), "cc": UnoCard("cc", "black", -3, True)
}
color_only_cards: dict[str, UnoCard] = {
    "greencc": UnoCard("gcc", "green", -4), "green+4": UnoCard("g+4", "green", -4),
    "bluecc": UnoCard("bcc", "blue", -4), "blue+4": UnoCard("b+4", "blue", -4),
    "redcc": UnoCard("rcc", "red", -4), "red+4": UnoCard("r+4", "red", -4),
    "yellowcc": UnoCard("ycc", "yellow", -4), "yellow+4": UnoCard("y+4", "yellow", -4)
}

default_deck: list[UnoCard] = []  # 76 Number Cards (19 each color), 24 Action cards(6 each color) and 8 wild cards

for color in ('b', 'y', 'g', 'r'):
    default_deck.append(all_cards[f"{color}0"])
    for _ in range(2):

        default_deck.append(all_cards["+4"])  # add wildcards
        default_deck.append(all_cards["cc"])

        for k in ("+2", "x", "<>"):
            default_deck.append(all_cards[f"{color}{k}"])

        for n in range(1, 10):
            default_deck.append(all_cards[f"{color}{n}"])


class UnoPlayer(Player):

    def __init__(self, discord_id: int, discord_user: User):
        super().__init__(discord_id)
        self.hand: list[UnoCard] = []
        self.discord_user = discord_user
        self.tie = False

    def display_hand(self) -> str:
        display = ""
        card_counts: dict[str, int] = {}

        for card in self.hand:

            try:

                card_counts[card.symbol] += 1

            except KeyError:

                card_counts[card.symbol] = 1

        for card in self.hand:

            display += f"**{card.display()} ({card.symbol})**x{card_counts[card.symbol]}"

        return display


class UnoGame(Game):

    def __init__(self, players: list[UnoPlayer]):
        super().__init__("Uno", 4, 2)
        random.shuffle(players)

        self.card_pickups = 0  # from +2/+4 cards
        self.players: list[UnoPlayer] = players
        self._deck: list[UnoCard] = self.new_deck()
        self.movement = 1  # 1 by default, multiplied by -1 every time a reverse card is dropped
        self.current_pos = 0
        self.ongoing = False
        self.timer = 0
        self.last_card: UnoCard or None = None

    def new_deck(self) -> list[UnoCard]:
        new_deck = default_deck.copy()
        random.shuffle(new_deck)
        return new_deck

    def current_player(self) -> UnoPlayer:
        return self.players[self.current_pos]

    def deal_cards(self):

        for player in self.players:  # shuffle cards to players (7 each)

            for _ in range(7):

                player.hand.append(self._deck[0])
                self._deck.pop(0)

        self.last_card = self._deck[0]
        self._deck.pop(0)

    def next_round(self, steps=1):
        self.timer = time()
        self.current_pos = self.step_to_player(distance=steps)

    def step_to_player(self, distance: int) -> int:
        """
        Find the player after distance turns from the current one
        """
        pos = self.current_pos

        for _ in range(distance):

            if pos + 1 == len(self.players) and self.movement == 1:  # to avoid index errors in the future
                pos = 0

            elif pos == 0 and self.movement == -1:
                pos = len(self.players) - 1

            else:
                pos += self.movement

        return pos

    def get_queue(self) -> list[UnoPlayer]:
        queue = []
        current_index = self.current_pos

        for _ in self.players:

            try:

                queue.append(self.players[current_index])

            except IndexError:

                if self.movement == 1:

                    queue.append(self.players[0])
                    current_index = 0

                else:

                    queue.append(self.players[len(self.players) - 1])
                    current_index = len(self.players) - 1

            current_index += 1 * self.movement

        return queue

    def take_card(self) -> UnoCard:

        if len(self._deck) > 0:

            top_card = self._deck[0]
            self._deck.pop(0)
            return top_card

        self._deck = self.new_deck()

        self.take_card()  # max recursions = 1

    def get_player_by_id(self, discord_id: int) -> UnoPlayer:
        """
        Call this function after you have checked whether or not this player is part of this game
        """
        for player in self.players:

            if player.discord_id == discord_id:

                return player
