"""
展示基本的 pygame 游戏循环
"""

import pygame as pg


def main():
    # 初始化设置
    pg.init()
    screen = pg.display.set_mode((1280, 900))
    clock = pg.time.Clock()
    running = True

    # 游戏主循环
    while running:
        # 事件处理逻辑
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # 背景颜色填充
        screen.fill("white")

        # 在此处渲染处理...

        # 翻转渲染内容到屏幕
        pg.display.flip()

        # 限制 FPS 到 60 帧
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
