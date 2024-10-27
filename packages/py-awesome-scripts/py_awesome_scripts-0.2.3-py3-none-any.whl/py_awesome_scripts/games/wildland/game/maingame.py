import pygame as pg

from game.base import BaseGame
from game.config import Config, DIR_MAP
from game.menu.main_menu import MainMenu
from game.tilemap import Map


class MainGame(BaseGame):
    """游戏类"""

    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.menu = MainMenu(self)
        self.map = Map(self, DIR_MAP / "map.txt")

    def play(self):
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return

                for button in self.group_buttons:
                    button.handle_event(event)

            self.update()
            self.draw()
            self.clock.tick(60)

    def update(self):
        # 更新精灵组
        self.groups.update()

    def draw(self):
        # 填充背景色
        self.screen.fill((0, 0, 0))
        dirty_rects = self.groups.draw(self.screen)
        pg.display.update(dirty_rects)
