import random
import time
import sys
import pygame
from pygame import mixer
from pygame.locals import *

if __name__ == '__main__':
    # Create the color variables
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Function to draw a button on the screen
    def button(screen, position, text):
        font = pygame.font.SysFont("Verdana", 50)
        text = font.render(text, bool(1), black)
        x, y, z, t = text.get_rect()
        x, y = position
        pygame.draw.line(screen, white, (x, y), (x + z, y), 5)
        pygame.draw.line(screen, white, (x, y - 2), (x, y + t), 5)
        pygame.draw.line(screen, white, (x, y + t), (x + z, y + t), 5)
        pygame.draw.line(screen, white, (x + z, y + t), [x + z, y], 5)
        pygame.draw.rect(screen, white, (x, y, z, t))

        return screen.blit(text, (x, y))

    # Create the enemy class
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("Enemy.png")
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(40, width - 40), 0)

        # Function for the enemy movement
        def move(self):
            global score
            self.rect.move_ip(0, enemy_speed)

            if self.rect.bottom > 600:
                score += 1
                self.rect.top = 0
                self.rect.center = (random.randint(40, width - 40), 0)

    # Create the player class
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("Player.png")
            self.rect = self.image.get_rect()
            self.rect.center = (160, 520)

        # Function for the player movement
        def move(self):
            pressed_keys = pygame.key.get_pressed()

            if self.rect.y > 0:
                if pressed_keys[K_UP]:
                    self.rect.move_ip(0, -1 * player_speed)

            if self.rect.y < height - 100:
                if pressed_keys[K_DOWN]:
                    self.rect.move_ip(0, player_speed)

            if self.rect.left > 0:
                if pressed_keys[K_LEFT]:
                    self.rect.move_ip(-1 * player_speed, 0)

            if self.rect.right < width:
                if pressed_keys[K_RIGHT]:
                    self.rect.move_ip(player_speed, 0)

    # Initialize the game engine
    pygame.init()

    # Set up the FPS
    fps = 60
    FramePerSec = pygame.time.Clock()

    # Create the screen variables
    width = 400
    height = 600

    # Set up the fonts
    font = pygame.font.SysFont("Verdana", 60)
    font_small = pygame.font.SysFont("Verdana", 30)
    game_over = font.render("Game Over!", True, black)

    # Set up the background image
    background = pygame.image.load("background.png")

    # Create the screen
    display_surface = pygame.display.set_mode((width, height))
    display_surface.fill(white)
    pygame.display.set_caption("Racing Cars")

    start = 1
    # The loop to control the restart functionality
    while start == 1:
        # Create the variables
        player_speed = 8
        enemy_speed = 5
        score = 0

        # Set up the Sprites
        player = Player()
        enemy = Enemy()

        # Create the Sprite groups
        enemies = pygame.sprite.Group()
        enemies.add(enemy)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        all_sprites.add(enemy)

        # Add a new user event
        inc_speed = pygame.USEREVENT + 1
        pygame.time.set_timer(inc_speed, 1000)

        # Load and start the background music
        mixer.init()
        mixer.music.load('background.wav')
        mixer.music.play(loops=-1)

        game = 1
        # Game Loop
        while game == 1:
            # Cycle through all events
            for event in pygame.event.get():
                if event.type == inc_speed:
                    enemy_speed += 0.5

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            display_surface.blit(background, (0, 0))
            scores = font_small.render(str(score), True, black)
            display_surface.blit(scores, (10, 10))

            # Move and re-draw all Sprites
            for entity in all_sprites:
                entity.move()
                display_surface.blit(entity.image, entity.rect)

            # Check if a collision occurs between the player and the enemy
            if pygame.sprite.spritecollideany(player, enemies):
                # End game screen arrangements
                start = 0
                mixer.music.stop()
                pygame.mixer.Sound('crash.wav').play()
                time.sleep(1)

                # Game Over Screen
                display_surface.fill(white)
                display_surface.blit(game_over, game_over.get_rect(center=display_surface.get_rect().center))
                pygame.display.update()

                # Get the highest score
                file = open("highest.txt", "r")
                highest = int(file.read())
                file.close()

                # Record the highest score
                if score > highest:
                    highest = score
                    file = open("highest.txt", "w")
                    file.write(str(highest))
                    file.close()

                # Score Screen
                pygame.time.wait(1500)
                score_info = font.render("Score: " + str(score), True, black)
                display_surface.fill(white)
                display_surface.blit(score_info, score_info.get_rect(center=display_surface.get_rect().center))
                pygame.display.update()

                # Highest Score Screen
                pygame.time.wait(1500)
                score_info = font.render("Highest: " + str(highest), True, black)
                display_surface.fill(white)
                display_surface.blit(score_info, score_info.get_rect(center=display_surface.get_rect().center))
                pygame.display.update()

                # End Screen
                pygame.time.wait(1500)
                display_surface.fill(white)
                b1 = button(display_surface, (148, 300), "Quit")
                b2 = button(display_surface, (108, 200), "Restart")
                pygame.display.update()

                end_screen = 1
                # End Screen Loop
                while end_screen == 1:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if b1.collidepoint(pygame.mouse.get_pos()):
                                for entity in all_sprites:
                                    entity.kill()

                                pygame.quit()
                                sys.exit()

                            elif b2.collidepoint(pygame.mouse.get_pos()):
                                start = 1
                                end_screen = 0
                                game = 0

                        pygame.display.update()

            pygame.display.update()
            FramePerSec.tick(fps)
