import pygame

class Settings():

    def __init__(self):
        #初始化游戏
        #屏幕设置
        self.screen_width = 1200
        self.screnn_height = 800
        self.bg_color = (230, 230, 230)

class Ship():

    def __init__(self, screen):

        #初始化飞船设置并初始化其位置
        self.screen = screen

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):

        "在指定位置绘制飞创"
        self.screen.blit(self.image, self.rect)