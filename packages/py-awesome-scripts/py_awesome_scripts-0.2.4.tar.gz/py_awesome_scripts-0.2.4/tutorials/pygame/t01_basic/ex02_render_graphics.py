"""
展示基本图形渲染
"""

import typing

import pygame as pg

SCREEN_SIZE = (800, 600)


def main():
    # 初始化设置
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    running: bool = True

    line_width: float = 1.0
    center_pos: typing.List[int, int] = [120, 120]
    radius: float = 10.0
    circle_pos = [50, 400]
    direction = 1.0

    # 游戏主循环
    while running:
        # 事件处理逻辑
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_KP_PLUS:
                    line_width = pg.math.clamp(line_width + 1.0, 1.0, 10.0)
                elif event.key == pg.K_KP_MINUS:
                    line_width = pg.math.clamp(line_width - 1.0, 1.0, 10.0)
                elif event.key == pg.K_r:
                    radius = pg.math.clamp(radius + 5.0, 5.0, 40.0)
                elif event.key == pg.K_t:
                    radius = pg.math.clamp(radius - 5.0, 5.0, 40.0)
                elif event.key == pg.K_RIGHT:
                    center_pos[0] += 10
                elif event.key == pg.K_LEFT:
                    center_pos[0] -= 10

        # 处理逻辑
        circle_pos[0] = pg.math.clamp(
            circle_pos[0] + 20 * direction, 0, SCREEN_SIZE[0]
        )
        if circle_pos[0] >= SCREEN_SIZE[0]:
            direction = -1.0
        elif circle_pos[0] <= 50:
            direction = 1.0

        # 背景颜色填充
        screen.fill("white")

        # 在此处渲染处理...
        pg.draw.line(screen, "red", (30, 100), (100, 100), int(line_width))
        pg.draw.circle(screen, "green", center_pos, 20, int(line_width))
        pg.draw.rect(
            screen, "blue", (150, 150, 200, 200), int(line_width), int(radius)
        )
        pg.draw.circle(screen, "orange", circle_pos, 30)

        # 翻转渲染内容到屏幕
        pg.display.flip()

        # 限制 FPS 到 60 帧
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
