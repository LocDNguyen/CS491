#!/usr/bin/env python3

import pygame
from pygame.locals import *
import random

from buttons import UIPlain, UIElement, draw_text
from gamestate import GameState
from highscore import set_highscore
from testscreen import title_screen, highscore, game_over, white
from sprites import PlayerSprite
from constants import *
from pause import *

pygame.init()

highscore_file = 'highscores.txt'

screen_width = 1000
screen_height = 800
center = screen_width / 2

clock = pygame.time.Clock()

pause = Pause(True)

rows = 1 #3
cols = 1 #7
alien_cooldown = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders Frontier')
bg = pygame.Surface(screen.get_size())
bg.fill((0, 0, 0))

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)

        self.reset(x, y, health)

    def update(self, dt):
        global pause
        self.sprites.update(dt)
        key = pygame.key.get_pressed()
        self.direction = self.getKey()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if (key[pygame.K_RIGHT] and self.rect.right < screen_width):
            self.rect.x += self.speed
        if key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if (key[pygame.K_DOWN] and self.rect.bottom < screen_height):
            self.rect.y += self.speed

        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > self.cooldown:
            laser = Laser(self.rect.centerx, self.rect.top)
            laser_group.add(laser)
            self.last_shot = time_now
        
        self.mask = pygame.mask.from_surface(self.image)

        self.check_collisions()

        for live in range(self.health_remaining - 1):
           x = 5 + (live * (self.live_image.get_size()[0]))
           screen.blit(self.live_image, (x, 8))

    def getKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP
    
    def check_collisions(self):
        collisions = pygame.sprite.spritecollide(self, alien_group, False, pygame.sprite.collide_mask)
        if collisions:
            for alien in collisions:
                alien.health -= alien.health
            self.health_remaining -= 1

    def reset(self, x, y, health):
        self.image = pygame.image.load("Sprites/jet.png").convert_alpha()
        self.live_image = pygame.transform.rotozoom(self.image, 0, 0.7)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.speed = 8
        self.cooldown = 600
        self.health_remaining = health
        self.score = 0
        self.laser2 = False
        self.power_up_time = 0
        self.alive = True
        self.sprites = PlayerSprite(self)
        self.direction = None


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = self.check_laser_image()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def check_collisions(self):
        collisions = pygame.sprite.groupcollide(alien_group, laser_group, False, True, pygame.sprite.collide_mask)
        if collisions and not spaceship.laser2:
            for alien in collisions:
                alien.health -= 1
        elif collisions and spaceship.laser2:
            for alien in collisions:
                alien.health -= 3

    def check_laser_image(self):
        if spaceship.laser2:
            self.image = pygame.image.load("Sprites/dual.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
        else:
            self.image = pygame.image.load("Sprites/sprite_0.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
        return self.image

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        self.check_collisions()
        # self.check_boss_collisions()


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/jet.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1
        self.health = health

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += self.move_direction
        if self.health <= 0:
            spaceship.score += 100
            self.kill()
        if spaceship.health_remaining <= 0:
            pause.setPause(pauseTime = 3, func = GameState.NAME)
            spaceship.alive = False
        #self.move_counter += 1
        # if abs(self.move_counter) > 75:
        #     self.move_direction *= -1
        #     self.move_counter *= self.move_direction
            
    def change_direction(self):
        for alien in alien_group:
            alien.rect.y += 8
            alien.move_direction *= -1
    def check_edges(self):
        screen_rect = screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    
class Alien_Still(pygame.sprite.Sprite):
    def __init__(self, x, y):

        super().__init__()
        # Draw the enemy
        self.image = pygame.image.load("Sprites/jet.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
class Alien_Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation):
        pygame.sprite.Sprite.__init__(self)
        self.orientation = orientation
        if self.orientation:
            self.image = pygame.image.load("Sprites/sprite_0.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.image = pygame.transform.rotate(self.image, 180)
        else:
            self.image = pygame.image.load("Sprites/sprite_0.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        if self.orientation:
            self.rect.y += 4
        else:
            self.rect.x -= 4
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.health_remaining -= 1
        if pygame.sprite.spritecollide(self, rock_group, False, pygame.sprite.collide_mask):
            self.kill()
        if pygame.sprite.spritecollide(self, rock_group_two, False, pygame.sprite.collide_mask):
            self.kill()

        if spaceship.health_remaining <= 0:
            pause.setPause(pauseTime = 3, func = GameState.NAME)
            spaceship.alive = False

class Rock_Hori(pygame.sprite.Sprite):
    def __init__(self, x, y):

        super().__init__()

        self.speed = 2

        self.image = pygame.image.load("Sprites/meteorite.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):

        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)
        #if pygame.sprite.spritecollide(self, spaceship_group, True):
        #    self.kill()

class Rock_Vert(pygame.sprite.Sprite):
    def __init__(self, x, y):

        super().__init__()

        self.speed = 2

        self.image = pygame.image.load("Sprites/meteorite.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):

        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)
        #if pygame.sprite.spritecollide(self, spaceship_group, True):
        #    self.kill()


spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_laser_group = pygame.sprite.Group()
rock_group = pygame.sprite.Group()
rock_group_two = pygame.sprite.Group()
all_enemy_lasers = pygame.sprite.Group()
alien_still_group = pygame.sprite.Group()
falling_lasers = pygame.sprite.Group()

spaceship = Spaceship(center, screen_height - 100, 100)
spaceship_group.add(spaceship)


def create_aliens():
        for row in range(rows):
            for col in range(cols):
                alien = Alien(100 + col * 100, 100 + row * 70, 1)
                alien_group.add(alien)
            
def edge_check():
    for alien in alien_group:
        if alien.check_edges():
            alien.change_direction()
            break

def showSprites():
    spaceship_group.draw(screen)
    laser_group.draw(screen)
    alien_group.draw(screen)
    alien_laser_group.draw(screen)
    rock_group.draw(screen)
    rock_group_two.draw(screen)
    all_enemy_lasers.draw(screen)
    falling_lasers.draw(screen)


def game_loop(screen, buttons):
    while True:
        screen.blit(bg, (0, 0))

        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.QUIT:
                return GameState.QUIT

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()

def play():
    run = True
    last_alien_shot = pygame.time.get_ticks()
    end_timer_for_first_laser_mech = pygame.time.get_ticks()
    ender_timer = pygame.time.get_ticks()
    create_aliens()
    pressedEscToBegin = True
    pausedText = False
    stop = 0
    move_on = 10
    stop_making = 0
    while run:
        dt = clock.tick(60) / 500.0
        time_now = pygame.time.get_ticks()
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if spaceship.alive:
                    pause.setPause(playerPaused=True)
                    pressedEscToBegin = False
                    if not pause.paused:
                        showSprites()
                        pausedText = False
                    else:
                        pausedText = True

            if event.type == pygame.QUIT:
                run = False

        if pressedEscToBegin:
            draw_text(screen_width, 450, "Press Escape to Begin", 37, white, screen)
        if pausedText:
            draw_text(screen_width, 450, "Paused", 37, white, screen)

        if not pause.paused:
            if time_now - last_alien_shot > alien_cooldown and len(alien_laser_group) < 5 and len(alien_group) > 0:
                shooting_alien = random.choice(alien_group.sprites())
                alien_laser = Alien_Laser(shooting_alien.rect.centerx, shooting_alien.rect.bottom, True)
                alien_laser_group.add(alien_laser)
                last_alien_shot = time_now

            if len(alien_group) == 0 and len(rock_group) == 0 and stop == 0:
                rockCover = Rock_Hori(screen_width + 40, 500)
                rock_group.add(rockCover)
            elif len(rock_group) == 1 and stop == 0:
                if time_now - end_timer_for_first_laser_mech > 300:
                    for row in range(1):
                        for item in range(50):
                            # Enemy(buffer to the left + pixels apart, buffer at the top + pixels apart)
                            laser = Alien_Laser((10 + item * 20), (2 + row * 50), True)
                            all_enemy_lasers.add(laser)
                    end_timer_for_first_laser_mech = time_now
                if rockCover.rect.left < 250:
                    stop += 1

            if stop == 1 and len(rock_group) == 0 and len(rock_group_two) == 0:
                rockCover = Rock_Vert(700, screen_height + 40)
                rock_group_two.add(rockCover)
            elif stop == 1 and len(rock_group_two) == 1:
                if time_now - end_timer_for_first_laser_mech > 200:
                    for row in range(1):
                        for item in range(40):
                            # Enemy(buffer to the left + pixels apart, buffer at the top + pixels apart)
                            laser = Alien_Laser((screen_width + row * 20), (2 + item * 50), False)
                            all_enemy_lasers.add(laser)
                    end_timer_for_first_laser_mech = time_now
                if rockCover.rect.top < 200:
                    stop += 1

            if stop == 2:
                if time_now - end_timer_for_first_laser_mech > 70:
                    if stop_making == 0:
                        for row in range(1):
                            for item in range(45):
                                # Enemy(buffer to the left + pixels apart, buffer at the top + pixels apart)
                                enemy = Alien_Still((10 + item * 20), (-20 + row * 50))
                                alien_still_group.add(enemy)
                            stop_making = 1
                    print(time_now - last_alien_shot)
                    print(len(all_enemy_lasers))
                    print(alien_cooldown)
                    if time_now - last_alien_shot > alien_cooldown and len(falling_lasers) < 200:
                        attacking_enemy = random.choice(alien_still_group.sprites())
                        enemy_laser = Alien_Laser(attacking_enemy.rect.centerx, attacking_enemy.rect.bottom, True)
                        falling_lasers.add(enemy_laser)
                        end_timer_for_first_laser_mech = time_now
                if move_on > 0:
                    if time_now - ender_timer > 2500:
                        move_on -= 1
                        ender_timer = time_now
                if move_on == 0:
                    alien_still_group.empty()
                    stop_making = 0
                    stop += 1

            laser_group.update()
            alien_group.update()
            alien_laser_group.update()
            all_enemy_lasers.update()
            rock_group.update()
            rock_group_two.update()
            falling_lasers.update()

        if spaceship.alive:
            if not pause.paused:
                spaceship_group.update(dt)
                showSprites()
        else:
            spaceship_group.update(dt)
            showSprites()

        afterPauseMethod = pause.update(dt)
        if afterPauseMethod is not None:
            if afterPauseMethod == GameState.NAME:
                return GameState.NAME
            afterPauseMethod()

        edge_check()

        pygame.display.update()
    return GameState.QUIT

def getting_name():
    user_text = ''
    global highscore_file
    font = pygame.font.SysFont('freesansbold.ttf', 37)
    input_rect = pygame.Rect(465, 305, 58, 35) #y normally 705

    running = True
    while running:

        screen.blit(bg, (0, 0))

        # Getting user input for name
        for event in pygame.event.get():   # for loop to check for a event trigger from pygames
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                if len(user_text) >= 4:
                    user_text = user_text[:-1]
                if event.key == pygame.K_RETURN:
                    set_highscore(highscore_file, user_text, spaceship.score)
                    return GameState.DEAD

        # Displaying what the user types in
        pygame.draw.rect(screen, white, input_rect, 2)
        text = font.render(user_text, True, white)
        screen.blit(text, (input_rect.x + 5, input_rect.y + 5))

        # Box around the user input moves with the input
        input_rect.w = max(10, text.get_width() + 10)

        pygame.display.update()  # update our screen
        # clock.tick(fps)

def main():
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen, center, game_loop)

        if game_state == GameState.NEWGAME:
            game_state = play()

        if game_state == GameState.HIGHSCORE:
            game_state = highscore(screen, highscore_file, center, game_loop)

        if game_state == GameState.DEAD:
            game_state = game_over(screen, screen_height, center, game_loop, spaceship, spaceship_group, laser_group, alien_group, alien_laser_group)

        if game_state == GameState.NAME:
            game_state = getting_name()

        if game_state == GameState.QUIT:
            pygame.quit()
            return 0

if __name__ == '__main__':
    main()