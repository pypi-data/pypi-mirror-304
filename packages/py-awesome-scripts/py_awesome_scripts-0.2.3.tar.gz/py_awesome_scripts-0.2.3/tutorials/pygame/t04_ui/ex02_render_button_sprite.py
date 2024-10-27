import sys

import pygame

# 初始化 Pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((640, 480))

# 设置字体和字号
font = pygame.font.Font(None, 36)


# 定义按钮类，继承自pygame.sprite.Sprite
class Button(pygame.sprite.Sprite):
    def __init__(
        self, text, position, width, height, bg_color, text_color, border_color
    ):
        super().__init__()
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.hover_color = (255, 255, 0)  # 悬停时的颜色
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect(topleft=position)
        self.text_surface = font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.hover = False  # 鼠标是否悬停的标志

    def update(self, mouse_pos):
        # 检查鼠标是否悬停在按钮上
        self.hover = self.rect.collidepoint(mouse_pos)
        self.image.fill(self.bg_color if not self.hover else self.hover_color)
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)


# 创建按钮
button = Button(
    "Click Me", (320, 240), 200, 50, (255, 255, 255), (255, 0, 0), (0, 0, 0)
)

# 创建一个sprite组来管理按钮
button_group = pygame.sprite.Group()
button_group.add(button)

# 游戏主循环
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()  # 获取鼠标位置
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景色
    screen.fill((0, 0, 0))

    # 更新按钮状态
    button_group.update(mouse_pos)

    # 更新屏幕显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
sys.exit()
