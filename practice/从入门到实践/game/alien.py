import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        "初始化外星人并设置其起始位置"
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/enemy.bmp')