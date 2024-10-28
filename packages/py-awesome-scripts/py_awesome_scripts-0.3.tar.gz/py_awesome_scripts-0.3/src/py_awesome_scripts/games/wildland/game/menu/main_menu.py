import pygame

from game.base import BaseGame
from game.menu.base import BaseMenu
from ui.button import ButtonAction, ButtonGroup
from ui.panel import Panel


class MainMenu(BaseMenu):
    def __init__(self, game: BaseGame):
        """
        :param game:
        """
        super().__init__(game, "main")

        Panel(self.game, (300, 200), 400, 300, border_color=(255, 0, 0))

        ButtonGroup(
            self.game,
            [
                ButtonAction("新游戏", None),
                ButtonAction("载入存档", None),
                ButtonAction("开始游戏", None),
                ButtonAction("排行榜", None),
                ButtonAction("退出", self.quit_game),
            ],
            (370, 240),
            200,
            40,
            20,
            border_color=(0, 255, 255),
        )

    def quit_game(self, event: pygame.event.Event):
        print(f"[*] 退出游戏, {event=}")
        self.game.quit()
