import typing

import pygame as pg

from game.base import BaseGame


class Panel(pg.sprite.DirtySprite):
    def __init__(
        self,
        game: BaseGame,
        pos: typing.Tuple[int, int],
        width: int,
        height: int,
        bg_color: typing.Tuple[int, int, int] = (121, 121, 121),
        border_color: typing.Tuple[int, int, int] = None,
        border_width: int = 2,
        border_radius: int = 4,
    ):
        super().__init__()

        self.game = game
        self.game.groups.add(self)

        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect(topleft=pos)
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius

    def update(self):
        if self.border_color is not None:
            draw_rect = self.image.get_rect(topleft=(0, 0))
            pg.draw.rect(
                self.image, self.bg_color, draw_rect, 0, self.border_width
            )
            pg.draw.rect(
                self.image,
                self.border_color,
                draw_rect,
                self.border_width,
                self.border_radius,
            )
