"""
通过 sprite 的运动参数, 展示牛顿运动学定律原理
"""

import pygame as pg

WIDTH = 1000
HEIGHT = 800
FPS = 80


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.Surface((60, 80))
        self.image.fill("yellow")

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        self.pos = pg.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)

    def update(self):
        self.acc = pg.math.Vector2(0, 0)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -0.2
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.2
        if keys[pg.K_UP]:
            self.acc.y = -0.2
        if keys[pg.K_DOWN]:
            self.acc.y = 0.2

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos


def draw_text(screen, text, size, col, x, y):
    """绘制文字"""
    font = pg.font.SysFont("SimHei", size)
    text_surface = font.render(text, True, col)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def draw_vec(screen, obj):
    """绘制运动向量"""
    if obj.vel.x != 0:
        draw_arrow(screen, obj.pos, (obj.pos + obj.vel * 20), "green", 7)

    if obj.acc.x != 0:
        pg.draw.circle(screen, "red", obj.pos, 10)
        draw_arrow(screen, obj.pos, (obj.pos + obj.acc * 400), "red", 3)


def draw_arrow(screen, p1, p2, col, size):
    """绘制箭头"""
    pg.draw.line(screen, col, p1, p2, size)

    if p2.x > p1.x:
        t1 = (p2.x + 5, p2.y)
        t2 = (p2.x - 10, p2.y + 10)
        t3 = (p2.x - 10, p2.y - 10)
    else:
        t1 = (p2.x - 5, p2.y)
        t2 = (p2.x + 10, p2.y + 10)
        t3 = (p2.x + 10, p2.y - 10)
    pg.draw.polygon(screen, col, [t1, t2, t3])


def main():
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("ex01_motion_demo")
    clock = pg.time.Clock()

    all_sprites = pg.sprite.Group()
    player = Player()
    all_sprites.add(player)

    running = True
    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        all_sprites.update()

        screen.fill("black")
        all_sprites.draw(screen)
        draw_vec(screen, player)
        txt = "Pos: ({:.2f}, {:.2f})".format(player.pos.x, player.pos.y)
        draw_text(screen, txt, 25, "white", 5, 5)
        txt = "Vel: ({:.2f}, {:.2f})".format(player.vel.x, player.vel.y)
        draw_text(screen, txt, 25, "green", 5, 55)
        txt = "Acc: ({:.2f}, {:.2f})".format(player.acc.x, player.acc.y)
        draw_text(screen, txt, 25, "red", 5, 105)
        draw_text(screen, f"FPS: {FPS}", 25, "purple", 5, 155)

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
