
class Player:

    occupied_players: list[int] = []  # all players, currently in a game

    def __init__(self, discord_id: int):
        self.discord_id: int = discord_id
