# 10.05.2020 Создание пришельца.
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс, представляющий одного пришельца."""
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load("Image/ufo.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width   # Каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        """Выводит пришельца в текущем положении."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Перемещает пришельца влево или вправо."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        # Влияние пременной fleet_direction оказывает на направление движения в зависимости от знака.
        self.rect.x = self.x

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        # Атрибут rect.right пришельца сравнивается с screen_rect.right экрана.
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True