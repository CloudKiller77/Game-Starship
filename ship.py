#  29.04.2020 Создание корабля.
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings, screen):
        super(Ship, self).__init__()
        """Инициализирует корабль и задает его начальную позицию."""
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load("Image/space_ship2.png")  # Функция для загрузки изображения
        self.rect = self.image.get_rect()   # Метод для получения атрибута изображения-поверхности (прямоугольника)
        self.screen_rect = screen.get_rect()   # Сохраняем прямоугольник на экране
        # self.rect.centery = self.screen_rect.centery  # Позиционирование относительно левого края окна.
        # self.rect.left = self.screen_rect.left
        self.rect.centerx = self.screen_rect.centerx    # Координаты центра игрового элемента по оси Х
        self.rect.bottom = self.screen_rect.bottom  # Координаты низа прямоугольника по оси У, по нижнему краю экрана
        self.center = float(self.rect.centery)
        self.bottom = float(self.rect.bottom)
        self.top = float(self.rect.top)
        self.moving_right = False
        self.moving_left = False
        self.moving_bottom = False
        self.moving_top = False

    def update(self):
        """Обновляет позицию корябля с учетом флага."""

        if self.moving_right and self.rect.right < 1200:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_top and self.rect.top > 0:
            self.bottom -= self.ai_settings.ship_speed_factor
        if self.moving_bottom and self.rect.bottom < 800:
            self.bottom += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom


    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)   # Вывод изображения на экран


    def center_ship(self):
        """Выравнивание корабля по центру."""
        self.center = self.screen_rect.centerx


class Ship2():
    pass