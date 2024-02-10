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

        # time_now = pygame.time.get_ticks()
        # if key[pygame.K_SPACE] and time_now - self.last_shot > self.cooldown:
        #     laser = Laser(self.rect.centerx, self.rect.top, self.alien_group, self.laser_group, self, self.big_boss_group)
        #     self.laser_group.add(laser)
        #     self.last_shot = time_now

        # if self.health_remaining <= 0:
        #     self.kill()
        #     return GameState.NAME
        
        self.mask = pygame.mask.from_surface(self.image)

        # self.check_collisions()

        #for live in range(self.health_remaining - 1):
        #    x = 5 + (live * (self.live_image.get_size()[0]))
        #    self.screen.blit(self.live_image, (x, 8))

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

spaceship_group = pygame.sprite.Group()
spaceship = Spaceship(center, screen_height - 100, 5)
spaceship_group.add(spaceship)

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
        spaceship_group.draw(screen)

        pygame.display.update()


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