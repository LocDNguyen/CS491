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

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders: Frontier')
bg = pygame.Surface(screen.get_size())
bg.fill((0, 0, 0))

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

def main():
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen, center, game_loop)

        # if game_state == GameState.NEWGAME:
        #     game_state = play()

        # if game_state == GameState.SECOND:
        #     game_state = play_two()

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