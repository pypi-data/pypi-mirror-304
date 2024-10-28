import pygame

from game.base import BaseGame
from game.menu.base import BaseMenu
from ui.button import ButtonAction, ButtonGroup


class RankingMenu(BaseMenu):
    def __init__(self, game: BaseGame):
        """
        :param game:
        """
        super().__init__(game, "ranking")

        ButtonGroup(
            self.game,
            [ButtonAction("返回主菜单", self.back_to_main)],
            (370, 240),
            200,
            40,
            20,
            border_color=(0, 255, 255),
        )

    def back_to_main(self, event: pygame.event.Event):
        print(f"[*] 返回主菜单, {event=}")
