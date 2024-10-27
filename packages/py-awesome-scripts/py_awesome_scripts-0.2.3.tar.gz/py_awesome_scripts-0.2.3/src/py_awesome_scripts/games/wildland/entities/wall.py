import pygame as pg

from game.base import BaseGame


class Wall(pg.sprite.DirtySprite):
    """墙壁"""

    def __init__(self, game: BaseGame, x: int, y: int):
        """
        :param game:
        :param x:
        :param y:
        """
        super().__init__()

        self.game = game
        self.game.groups.add(self, layer=-1)

        self.image = pg.Surface((self.game.tile_size, self.game.tile_size))
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.pos = pg.Vector2(x, y)

    def update(self):
        self.rect.topleft = (
            self.pos.x * self.game.tile_size,
            self.pos.y * self.game.tile_size,
        )
