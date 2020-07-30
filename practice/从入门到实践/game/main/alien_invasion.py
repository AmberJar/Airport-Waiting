import pygame
from practice.从入门到实践.game.game_stats import GameStats
from practice.从入门到实践.game.settings import Settings
from practice.从入门到实践.game.ship import Ship
from practice.从入门到实践.game.button import Button
from practice.从入门到实践.game.scroeboard import Scoreboard
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

    #创建PLAY按钮
    play_button = Button(ai_settings, screen, "Play")

    #创建储存游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

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
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()