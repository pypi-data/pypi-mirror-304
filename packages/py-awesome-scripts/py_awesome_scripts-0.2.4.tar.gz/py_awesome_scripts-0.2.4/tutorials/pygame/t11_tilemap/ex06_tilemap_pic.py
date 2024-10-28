import pathlib
import sys
import typing

import pygame as pg

vec = pg.math.Vector2

# 游戏基本设置
GameSettings = typing.NamedTuple(
    "GameSettings",
    (
        ("size", typing.Tuple[int, int]),
        ("title", str),
        ("tile_size", int),
        ("fps", int),
        ("speed", float),
        ("hit_rect", pg.Rect),
    ),
)

GS: GameSettings = GameSettings(
    size=(1024, 768),
    title="Tile Map Basic",
    tile_size=64,
    fps=120,
    speed=300,
    hit_rect=pg.Rect(0, 0, 35, 35),
)

DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
CWD = pathlib.Path(__file__).parent


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(GS.size)
        pg.display.set_caption(GS.title)

        # 基本参数
        self.clock = pg.time.Clock()
        self.dt: float = 0.0
        self.map = Map(pathlib.Path(__file__).parent / "assets" / "map3.txt")
        self.camera: Camera = None

        # sprite groups
        self.group_wall: pg.sprite.Group = None
        self.group_all: pg.sprite.Group = None

        # sprite
        self.player: pg.sprite.Sprite = None
        self.player_img = pg.image.load(
            CWD / "assets" / "img" / "manBlue_gun.png"
        ).convert_alpha()

    def setup(self):
        self.group_all = pg.sprite.Group()
        self.group_wall = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        while True:
            self.dt = self.clock.tick(GS.fps) / 1000
            self.events()
            self.update()
            self.draw()

    @staticmethod
    def quit():
        pg.quit()
        sys.exit()

    def update(self):
        self.group_all.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, GS.size[0], GS.tile_size):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, GS.size[1]))
        for y in range(0, GS.size[1], GS.tile_size):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (GS.size[0], y))

    def draw(self):
        self.screen.fill(DARKGREY)
        self.draw_grid()

        # 根据camera渲染
        for sprite in self.group_all:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


class Player(pg.sprite.Sprite):
    def __init__(self, game: Game, x: int, y: int):
        super().__init__(game.group_all)

        self.game = game

        # 处理sprite
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = GS.hit_rect
        self.hit_rect.center = self.rect.center

        self.vel = vec(0, 0)
        self.pos = vec(x, y) * GS.tile_size
        self.rot = 0
        self.rot_speed = 0.0

    def get_keys(self):
        # 初始化速度
        self.rot_speed = 0
        self.vel = vec(0, 0)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot = GS.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot = -GS.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(GS.speed, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-GS.speed / 2, 0).rotate(-self.rot)

    def collide_with_walls(self, direction: str):
        if hits := pg.sprite.spritecollide(
            self,
            self.game.group_wall,
            False,
            lambda x, y: x.hit_rect.colliderect(y.rect),
        ):
            if direction == "x":
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2.0
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2.0
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
            if direction == "y":
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2.0
                if self.vel.y < 0:
                    self.pos.y = (
                        hits[0].rect.bottom + self.hit_rect.height / 2.0
                    )
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def update(self) -> None:
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls("x")
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls("y")
        self.rect.center = self.hit_rect.center


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


class Map:
    def __init__(self, filename: str):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())

        self.tile_width = len(self.data[0])
        self.tile_height = len(self.data)
        self.width = self.tile_width * GS.tile_size
        self.height = self.tile_height * GS.tile_size


class Camera:
    def __init__(self, width: int, height: int):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity: pg.sprite.Sprite):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(GS.size[0] / 2)
        y = -target.rect.y + int(GS.size[1] / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - GS.size[0]), x)  # right
        y = max(-(self.height - GS.size[1]), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)


def main():
    g = Game()

    while True:
        g.setup()
        g.run()


if __name__ == "__main__":
    main()
