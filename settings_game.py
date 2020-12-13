class Settings():
    """Класс для хранения настроек для всей игры."""

    def __init__(self):
        """Инициализируем настройки игры."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 66)
        self.ship_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (130, 60, 40)
        self.bullets_allowed = 5
        self.fleet_drop_speed = 50  # Движение вниз, по оси у.
        self.speedup_scale = 1.1  # Тем роста скорости игры.
        self.score_scale = 1.5  # Тем роста стоимости подьитого пришельца.
        self.aliens_points = 0
        self.initialize_dinamic_settings()


    def initialize_dinamic_settings(self):
        """Изменяемые по ходу игры настройки"""
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1  # Движение вправо или влево.
        self.fleet_direction = 1  # 1 обозначает движение вправо, -1 движение влево.
        self.aliens_points = 5

    def increase_speed(self):
        """Повышение сложности игры"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.aliens_points = int(self.aliens_points * self.score_scale)
        print(self.aliens_points)
