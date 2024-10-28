from game.base import BaseGame


class BaseMenu:
    def __init__(self, game: BaseGame, name: str):
        self.game = game
        self.name = name
