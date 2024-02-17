#!/usr/bin/env python3

import pygame

from buttons import UIPlain, UIElement
from gamestate import GameState
#from highscore import set_highscore
from testscreen import title_screen, highscore

pygame.init()

highscore_file = 'highscores.txt'

screen_width = 1000
screen_height = 800
center = screen_width / 2

clock = pygame.time.Clock()
fps = 60

rows = 3
cols = 7
alien_cooldown = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders Frontier')
bg = pygame.Surface(screen.get_size())
bg.fill((0, 0, 0))

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)

        self.reset(x, y, health)

    def update(self):

        key = pygame.key.get_pressed()
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

        # if self.health_remaining <= 0:
        #     self.kill()
        #     return GameState.NAME
        
        self.mask = pygame.mask.from_surface(self.image)

        # self.check_collisions()

        for live in range(self.health_remaining - 1):
           x = 5 + (live * (self.live_image.get_size()[0]))
           screen.blit(self.live_image, (x, 8))

    # def check_collisions(self):
    #     collisions = pygame.sprite.spritecollide(self, self.alien_group, False, pygame.sprite.collide_mask)
    #     if collisions:
    #         for alien in collisions:
    #             alien.health -= alien.health
    #         self.health_remaining -= 1


    def reset(self, x, y, health):
        self.image = pygame.image.load("Sprites/jet.png").convert_alpha()
        self.live_image = pygame.transform.rotozoom(self.image, 0, 0.7)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.speed = 8
        self.cooldown = 700
        self.health_remaining = health
        self.score = 0
        self.laser2 = False
        self.power_up_time = 0


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

    # def check_boss_collisions(self):
    #     collisions = pygame.sprite.groupcollide(self.big_boss_group, self.laser_group, False, True, pygame.sprite.collide_mask)
    #     if collisions and not self.spaceship.laser2:
    #         for boss in collisions:
    #             boss.health -= 1
    #     elif collisions and self.spaceship.laser2:
    #         for boss in collisions:
    #             boss.health -= 3

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
    

spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

spaceship = Spaceship(center, screen_height - 100, 5)
spaceship_group.add(spaceship)
def create_aliens():
        for row in range(rows):
            for col in range(cols):
                alien = Alien(100 + col * 100, 100 + row * 70, 4)
                alien_group.add(alien)
            
def edge_check():
    for alien in alien_group:
        if alien.check_edges():
            alien.change_direction()
            break

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
    create_aliens()
    while run:
        clock.tick(fps)
        time_now = pygame.time.get_ticks()
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #     game_pause()
            if event.type == pygame.QUIT:
                run = False

        spaceship_group.update()
        laser_group.update()
        alien_group.update()

        spaceship_group.draw(screen)
        laser_group.draw(screen)
        alien_group.draw(screen)

        edge_check()

        pygame.display.update()
    return GameState.QUIT


def main():
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen, center, game_loop)

        if game_state == GameState.NEWGAME:
            game_state = play()

        if game_state == GameState.HIGHSCORE:
            game_state = highscore(screen, highscore_file, center, game_loop)

        # if game_state == GameState.DEAD:
        #     game_state = game_over()

        # if game_state == GameState.NAME:
        #     game_state = getting_name()

        if game_state == GameState.QUIT:
            pygame.quit()
            return 0

if __name__ == '__main__':
    main()