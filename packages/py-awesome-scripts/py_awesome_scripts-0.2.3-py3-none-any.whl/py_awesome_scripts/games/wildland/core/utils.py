import typing
from typing import Tuple

import pygame as pg

from game.config import DIR_IMG


def convert_color(x: int) -> Tuple[int, int, int]:
    """转化 hex 格式为 tuple 格式."""
    return (x & 0xFF0000) >> 16, (x & 0xFF00) >> 8, (x & 0xFF)


def inverse_color(
    color: typing.Tuple[int, int, int],
) -> typing.Tuple[int, int, int]:
    """计算给定颜色的反色（互补色）"""
    return 255 - color[0], 255 - color[1], 255 - color[2]


def load_image(file):
    """loads an image, prepares it for play"""
    file = DIR_IMG / file
    try:
        surface = pg.image.load(str(file))
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()


def load_sound(file):
    """because pygame can be compiled without mixer."""
    if not pg.mixer:
        return None
    file = DIR_ASSETS / "music" / file
    try:
        sound = pg.mixer.Sound(str(file))
        return sound
    except pg.error:
        print(f"Warning, unable to load, {file}")
    return None
