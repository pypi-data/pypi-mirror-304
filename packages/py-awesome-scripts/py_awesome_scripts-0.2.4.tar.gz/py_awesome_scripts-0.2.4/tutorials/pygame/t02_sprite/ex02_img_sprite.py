"""
载入图片的 sprite 示例
"""

import pathlib
import random

import pygame as pg

WIDTH = 800
HEIGHT = 600

CWD = pathlib.Path(__file__).parent
AST = CWD / "assets"


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # 载入图片
        self.image = pg.image.load(AST / "p1_jump.png").convert()
        self.image.set_colorkey("black")

        # 设置 rect
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        self.y_speed = 5

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed * random.random()

        if self.rect.bottom > HEIGHT - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.left > WIDTH:
            self.rect.right = 0


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("ex02_img_sprite")
    clock = pg.time.Clock()

    all_sprites = pg.sprite.Group()
    player = Player()
    all_sprites.add(player)

    running = True
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        all_sprites.update()
        screen.fill("black")
        all_sprites.draw(screen)

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
