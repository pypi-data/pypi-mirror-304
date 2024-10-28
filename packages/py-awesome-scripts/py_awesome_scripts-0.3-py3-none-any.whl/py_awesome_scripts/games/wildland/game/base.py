import logging

import pygame as pg

from game.config import Config, DIR_FONT


class BaseGame:
    """游戏基类"""

    def __init__(self, config: Config):
        self.config = config
        self.screen: pg.Surface = None
        self.clock = pg.time.Clock()
        self.is_running = True

        self.groups = pg.sprite.LayeredDirty()
        self.group_buttons = pg.sprite.LayeredDirty()

        self._setup()

        font_size = self.config["ui"]["font_size"]
        font_file = self.config["ui"]["font"]
        self.font = pg.font.SysFont(font_file, font_size)

        self.tile_size = self.config["map"]["tile_size"]
        self.tile_x = self.config["map"]["tile_x"]
        self.tile_y = self.config["map"]["tile_y"]

    def _setup(self):
        if pg.get_sdl_version()[0] == 2:
            pg.mixer.pre_init(44100, 32, 2, 1024)

        pg.init()
        if pg.mixer and not pg.mixer.get_init():
            logging.debug("[*] 提示: 未找到声音设备")
            pg.mixer = None

        win_size = self.config["window"]["size"]
        best_depth = pg.display.mode_ok(win_size, 0, 32)
        self.screen = pg.display.set_mode(win_size, 0, best_depth)

        caption = self.config["window"]["caption"]
        pg.display.set_caption(caption)

    def quit(self):
        self.is_running = False
