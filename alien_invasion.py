import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Class for managing sourses and game behaviour"""

    def __init__(self):
        """ Initialize game and create game resourses
        pygame.display.set_mode() создает окно, в котором
        прорисовываются все графические элементы игры.
        Аргумент (1200, 800) - размер окна. """
        pygame.init()
        self.settings = Settings()

        # Start game in window or full screen
        if not self.settings.full_screen_mode:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        elif self.settings.full_screen_mode:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height

        # Name of the Game Window
        pygame.display.set_caption('Alien Invasion  - press q to exit - ')

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        # create score board
        self.sb = Scoreboard(self)

        # paint the ship
        self.ship = Ship(self)

        # paint bullets
        self.bullets = pygame.sprite.Group()

        # paint Aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play ! ")

    def _ship_hit(self):
        """ Respond to the ship being hit """
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_fleet_edges(self):
        """ Respond appropriately if any aliens have reached an edge """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and change the fleet's direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """ Create the fleet of aliens """
        # Make an alien.
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width
        number_aliens_x = available_space_x // (alien_width * 4)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (7 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row.
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + alien_width * 4 * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 5 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):
        """Start the main loop for the game!"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alliens()

            self._update_screen()

    def _update_alliens(self):
        """Check if the fleet is at an edge,
         then update the positions of all aliens in the fleet.
         """
        self._check_fleet_edges()
        """ Update the position"""
        self.aliens.update()
        # look for alien shi[ collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _update_bullets(self):
        """ Update position of bullets and get rid of old ones"""
        self.bullets.update()

        # get rid of old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def  _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliiens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliiens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
        # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()



    def _update_screen(self):
        # При каждом переходе цикла перерисовывается экран
        # self.screen.fill(self.settings.bg_colour)

        self.image = pygame.image.load('images/earth.png')
        self.rect = self.image.get_rect()
        self.screen.blit(self.image, self.rect)
        self.aliens.draw(self.screen)

        # Score info
        self.sb.show_score()

        # paint the ship
        self.ship.blitme()
        # bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw the play button
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drown screen visible
        pygame.display.flip()

    def _check_events(self):
        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Переместить корабль вправо \ влево
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game stats
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet / center the ship
            self._create_fleet()
            self.ship.center_ship()

    def _check_key_up_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_key_down_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        # exit game
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


if __name__ == '__main__':
    # Make the game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
