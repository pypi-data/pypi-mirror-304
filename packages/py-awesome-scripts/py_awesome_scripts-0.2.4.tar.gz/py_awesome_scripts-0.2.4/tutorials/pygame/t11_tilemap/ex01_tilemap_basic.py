import sys
import typing

import pygame as pg

# 游戏基本设置
GameSettings = typing.NamedTuple(
    "GameSettings",
    (
        ("size", typing.Tuple[int, int]),
        ("title", str),
        ("tile_size", int),
        ("fps", int),
    ),
)

GS: GameSettings = GameSettings(
    size=(800, 600),
    title="Tile Map Basic",
    tile_size=32,
    fps=120,
)

DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(GS.size)
        pg.display.set_caption(GS.title)

        # 基本参数
        self.clock = pg.time.Clock()

        # sprite groups
        self.group_wall: pg.sprite.Group = None
        self.group_all: pg.sprite.Group = None

        # sprite
        self.player: pg.sprite.Sprite = None

    def setup(self):
        self.group_all = pg.sprite.Group()
        self.group_wall = pg.sprite.Group()

        self.player = Player(self, 10, 10)
        for x in range(10, 20):
            Wall(self, x, 5)

    def run(self):
        while True:
            self.clock.tick(GS.fps)
            self.events()
            self.update()
            self.draw()

    @staticmethod
    def quit():
        pg.quit()
        sys.exit()

    def update(self):
        self.group_all.update()

    def draw_grid(self):
        for x in range(0, GS.size[0], GS.tile_size):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, GS.size[1]))
        for y in range(0, GS.size[1], GS.tile_size):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (GS.size[0], y))

    def draw(self):
        self.screen.fill(DARKGREY)
        self.draw_grid()
        self.group_all.draw(self.screen)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)


class Player(pg.sprite.Sprite):
    def __init__(self, game: Game, x: int, y: int):
        super().__init__(game.group_all)

        self.game = game

        # 处理sprite
        self.image = pg.Surface((GS.tile_size, GS.tile_size))
        self.image.fill("yellow")
        self.rect = self.image.get_rect()
        self.x, self.y = x, y

    def move(self, dx: int = 0, dy: int = 0):
        self.x += dx
        self.y += dy

    def update(self) -> None:
        self.rect.topleft = self.x * GS.tile_size, self.y * GS.tile_size


class Wall(pg.sprite.Sprite):
    def __init__(self, game: Game, x: int, y: int):
        super().__init__(game.group_all, game.group_wall)

        self.game = game

        # 处理sprite
        self.image = pg.Surface((GS.tile_size, GS.tile_size))
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.x, self.y = x, y

    def update(self) -> None:
        self.rect.topleft = self.x * GS.tile_size, self.y * GS.tile_size


def main():
    g = Game()

    while True:
        g.setup()
        g.run()


if __name__ == "__main__":
    main()
