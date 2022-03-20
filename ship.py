import pygame

class Ship:
    """A class to manage the ship """
    def __init__(self, ai_game):
        # инициализирует корабль и задаёт нач позицию
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        #  Загружает изобр корабля и получает прямоугольник
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        # each new ship appears in bottom edge
        self.rect.midbottom = self.screen_rect.midbottom
        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def update(self):
        """Обновляет позицию коробля с учётом флага
        self.moving_right = False"""
        # Update the ship's x value, not the rect.
        # self.rect.right / self.rect.left - right / left edge of the ship
        # self.screen_rect.right -edge of the screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.height:
            self.y += self.settings.ship_speed


        # Update rect object from self.x.
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """ Paints the ship in current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = self.settings.screen_height - 120
