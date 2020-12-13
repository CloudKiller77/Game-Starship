# 29.04.2020 Модуль управление событиями.

import sys
import json
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien



def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets):
    """Реагирует на нажатие клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_top = True
    elif event.key == pygame.K_DOWN:
        ship.moving_bottom = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Создает новую пулю, если максимум еще не достигнут."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_top = False
    elif event.key == pygame.K_DOWN:
        ship.moving_bottom = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Обрабатывает нажатие клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            filename = "high_score.txt"
            with open(filename, 'w', encoding='utf-8') as f_obj:
                f_obj.write(str(stats.high_score))
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play мышью."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dinamic_settings()  # настройки игры по умолчанию
        pygame.mouse.set_visible(False)  # Скрывает указатель мыши
        stats.reset_stats()  # Сброс игровой статистики
        stats.game_active = True
        # Сброс счета и уровня сложности при нажатие на кнопку.
        sb.prep_score()
        # sb.prep_hight_score()
        sb.prep_level()
        sb.prep_ships()
        # Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)  # Создание нового флота пришельцев
        ship.center_ship()  # Создание нового корабля по центру


def start_game(ai_settings, screen, stats, ship, aliens, bullets):
    """Запускает новую игру при нажатии кнопки P"""
    pygame.mouse.set_visible(False)  # Скрывает указатель мыши
    stats.reset_stats()  # Сброс игровой статистики
    stats.game_active = True
    # Очистка списков пришельцев и пуль
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)  # Создание нового флота пришельцев
    ship.center_ship()  # Создание нового корабля по центру


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обновление позиции пули и уничтожает старые пули."""
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Проверка попаданий в пришельцев. При обнаружениии попадания удалить пулю и пришельца."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # Метод сравнивает прямоугольник rect каждой пули с прямоугольником rect каждого пришельца и возвращает словарь
    # с пулями и пришельцами между которыми были обнаружены коллизии. Каждый ключ в словаре представляет пулю,
    # а значение пришельца, в которого попала пуля.
    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.aliens_points * len(collisions)  # Начисление очков за каждого сбитого пришельца.
            sb.prep_score()  # Вывод на экран текущего счета.
            check_high_score(stats, sb)  # Оюновление рекордного счета в лайв-режиме.
    if len(aliens) == 0:
        # Уничтожение существующих пуль empty() и создание нового флота.
        bullets.empty()
        ai_settings.increase_speed()  # повышение сложности игры
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)



def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображения на экране и отображает новый экран."""
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет колличество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height - (5 * alien_height) - ship_height)   # Определяем колличество рядов
    number_rows = int(available_space_y / (2 * alien_height))   # Вычисляем колличество пришельцев в рядах
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляем колличество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - (2 * alien_width) - 150
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.top > screen_rect.bottom:
            # Происходит то же, что и при столкновении с кораблем.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, aliens, ship, stats, sb, bullets):
    """Проверяет достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте."""
    check_fleet_edges(ai_settings, aliens)  # Проверяет достиг ли флот края, опускает его и меняет напрвление движения.
    aliens.update()   # Обновляет позиции всех пришельцев.
    # Проверка коллизий пришелец-корабль
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # Проверка пришельцев добравшихся до нижнего края экрана.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():  # для каждого пришельца функция проверяет его позицию относительно края экрана.
            change_fleet_direction(ai_settings, aliens)
            # Если check_edges(True) вызывается функция которая опускает флот и меняет направление движения
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцами."""
    if stats.ship_left > 0:
        stats.ship_left -= 1
        aliens.empty()
        bullets.empty()
        sb.prep_ships()
        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()  # Выравнивание нового корабля по центру
        # Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)




