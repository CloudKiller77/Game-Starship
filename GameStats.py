# 30.05.2020 Сбор статистики по игре.

class GameStats():
    """Отслеживание статистики по игре"""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False  # Игра Game_starship запускается в пассивном состоянии
        self.high_score = 0
        self.score = 0
        self.record_score()



    def record_score(self):
        """Считывает рекордный счет из файла."""
        filename = "high_score.txt"
        with open(filename) as f_obg:
            record = f_obg.read()
            self.high_score = int(record)



    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1