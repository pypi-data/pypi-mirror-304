import array
import typing

from entities.wall import Wall
from game.base import BaseGame


class Map:
    def __init__(self, game: BaseGame, filename: str):
        self.game = game
        self.data: array.array = array.array("b", [])
        self.filename = filename

        with open(filename, "rt") as f:
            for line in f:
                self.data.extend(bytearray(line.strip(), "ascii"))

        self.tile_width = self.game.tile_x
        self.tile_height = self.game.tile_y
        self.width = self.tile_width * self.game.tile_size
        self.height = self.tile_height * self.game.tile_size

        for i, tile in enumerate(self.data):
            col, row = i % self.game.tile_size, i // self.game.tile_size
            if tile == 49:
                Wall(self.game, col, row)

    def __getitem__(self, pos: typing.Tuple[int, int]):
        row, col = pos
        return self.data[row * self.tile_width + col]

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return f"filename={self.filename}, width={self.tile_width}, height={self.tile_height}\n"
