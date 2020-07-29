import pygame
from practice.从入门到实践.game.game_stats import GameStats
from practice.从入门到实践.game.settings import Settings
from practice.从入门到实践.game.ship import Ship
import practice.从入门到实践.game.game_functions as gf

from pygame.sprite import Group

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    stats = GameStats(ai_settings)

    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建一个用于储存的编组
    bullets = Group()
    aliens = Group()

    #创建一群外星人
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets)

run_game()