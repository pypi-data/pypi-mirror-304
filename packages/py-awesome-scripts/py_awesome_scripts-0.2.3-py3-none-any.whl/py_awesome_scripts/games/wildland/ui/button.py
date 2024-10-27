import typing

import pygame as pg

from core.utils import inverse_color
from game.base import BaseGame

ButtonAction = typing.NamedTuple(
    "ButtonAction",
    (("text", str), ("on_click", typing.Callable[[pg.event.Event], bool])),
)


class Button(pg.sprite.DirtySprite):
    """常规按键"""

    def __init__(
        self,
        game: BaseGame,
        text: str,
        pos: (int, int),
        width: int,
        height: int,
        bg_color: typing.Tuple[int, int, int] = (255, 255, 255),
        text_color: typing.Tuple[int, int, int] = (0, 255, 0),
        border_color: typing.Tuple[int, int, int] = None,
        on_click: typing.Callable[[pg.event.Event], bool] = None,
    ) -> None:
        """
        :param game: 所属游戏基类
        :param text: 文本
        :param pos: 位置
        :param width: 宽度
        :param height: 高度
        :param bg_color: 背景颜色
        :param text_color: 文本颜色
        :param border_color: 外框颜色
        :param on_click: 点击事件
        """
        super().__init__()

        self.game = game
        self.game.groups.add(self, layer=9)
        self.game.group_buttons.add(self)

        self.text = text
        self.pos = pos
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.on_click = on_click

        self.hover_color = inverse_color(pg.Color(bg_color))
        self.hover = False

        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect(topleft=pos)

        self.text_surface = self.game.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(
            center=(self.width / 2, self.height / 2)
        )

    def update(self):
        # 背景
        if self.bg_color:
            self.image.fill(
                self.bg_color if not self.hover else self.hover_color
            )

        # 边框
        if self.border_color:
            pg.draw.rect(self.image, self.border_color, self.rect, 4)

        # 文字
        self.image.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if callable(self.on_click):
                    self.on_click(event)
                else:
                    print(f"[*] 未配置按键事件函数: {self.text=}, {__file__=}")
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if not self.hover:
                    self.hover = True
                    self.dirty = True
            else:
                if self.hover:
                    self.hover = False
                    self.dirty = True


class ButtonGroup:
    """按键组, 用于并排组织按键"""

    def __init__(
        self,
        game: BaseGame,
        actions: typing.List[ButtonAction],
        pos: typing.Tuple[int, int],
        width: int,
        height: int,
        spacing: int,
        direction: str = "y",
        bg_color: typing.Tuple[int, int, int] = (255, 255, 255),
        text_color: typing.Tuple[int, int, int] = (0, 255, 0),
        border_color: typing.Tuple[int, int, int] = (255, 255, 255),
    ):
        """
        :param game:
        :param actions:
        :param pos:
        :param width:
        :param height:
        :param spacing:
        :param direction:
        :param bg_color:
        :param text_color:
        :param border_color:
        """
        self.game = game
        self.actions: typing.List[ButtonAction] = actions
        self.buttons: typing.List[Button] = []

        for i, action in enumerate(actions):
            if direction == "y":
                btn_pos = pos[0], pos[1] + i * (height + spacing)
            else:
                btn_pos = pos[0] + i * (width + spacing), pos[1]

            self.buttons.append(
                Button(
                    self.game,
                    action.text,
                    btn_pos,
                    width=width,
                    height=height,
                    bg_color=bg_color,
                    text_color=text_color,
                    border_color=border_color,
                    on_click=action.on_click,
                )
            )
