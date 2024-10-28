"""
基本 Sprite 创建与使用
"""

import pygame as pg
import random

SCREEN_SIZE = (800, 600)


class Player(pg.sprite.Sprite):
    def __init__(self):
        # 需要调用父类构造函数
        super().__init__()

        # 创造一个 surface 用于显示 sprite
        self.image = pg.Surface((50, 50))
        self.image.fill((0, 255, 0))

        # 设置 sprite 对应包含矩形
        self.rect = self.image.get_rect()
        # 设置 sprite 中心
        self.rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)

    def update(self):
        # 在每次游戏循环更新时都会变动
        self.rect.center = pg.mouse.get_pos()

    def collide(self, other: pg.sprite.Sprite):
        # 判断与其他 sprite 是否交叉
        return self.rect.colliderect(other.rect)


class MovingRect(pg.sprite.Sprite):
    SPEED = 10

    def __init__(self):
        super().__init__()

        self.image = pg.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)

        self.direction = 1.0

    def update(self):
        self.rect.x += random.randint(0, self.SPEED) * self.direction
        if self.rect.right > SCREEN_SIZE[0] or self.rect.left < 0:
            self.direction = -self.direction


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("ex01_single_sprite")
    clock = pg.time.Clock()
    running = True

    # 创建 sprite 分组
    all_sprites = pg.sprite.Group()
    player: Player = Player()
    moving_rect: MovingRect = MovingRect()
    all_sprites.add(player)
    all_sprites.add(moving_rect)

    while running:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # 更新 sprites
        all_sprites.update()
        screen.fill("black")
        all_sprites.draw(screen)

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
