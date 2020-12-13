# 28.04.2020 PyGame создание игры.
import pygame
from pygame.sprite import Group
import sys
from settings_game import Settings
from GameStats import GameStats
from scoreboard import Scoreboard
from Button import Button
from ship import Ship
from alien import Alien
import game_functions as gf


def run_game():
    """Инициализирует игру и создает объект экрана."""

    pygame.init()
    ai_settings = Settings()   # Импортируем класс параметры игрового окна.
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Warriors")
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)  # Импортируем класс статистики
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)  # Импортируем класс корабля
    alien = Alien(ai_settings, screen)  # Импортируем класс пришельца
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        """Отслеживание событий клавиатуры и мыши."""
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)   # Импортируем модуль управление событиями

        if stats.game_active:
            ship.update()    # Создает космический корабль
            bullets.update()    # Создает новые пули
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)     # Ограничивает колличество выпущенных пуль
            gf.update_aliens(ai_settings, screen, aliens, ship, stats, sb, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)   # Управление обновлением экрана


run_game()