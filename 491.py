#!/usr/bin/env python3

import pygame
from pygame.sprite import RenderUpdates

from buttons import UIPlain, UIElement
from gamestate import GameState
from highscore import get_highscore, set_highscore
pygame.init()

white = (255, 255, 255)
green = (255, 0, 255)
red = (255, 0, 0)
blue = (0, 255, 255)

highscore_file = 'highscores.txt'

screen_width = 1000
screen_height = 800

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

from buttons import UIPlain, UIElement

def title_screen(screen):
    # title =  UIPlain(center_position = (400, 160), font_size = 140, text_rgb = red, text = "SPACE")
    # title_2 =  UIPlain(center_position = (400, 290), font_size = 140, text_rgb = red, text = "INVADERS")
    title_3 =  UIPlain(center_position = (500, 160), font_size = 140, text_rgb = white, text = "SPACE")
    title_4 =  UIPlain(center_position = (500, 290), font_size = 140, text_rgb = white, text = "INVADERS")
    title_5 =  UIPlain(center_position = (510, 170), font_size = 140, text_rgb = blue, text = "SPACE")
    title_6 =  UIPlain(center_position = (510, 300), font_size = 140, text_rgb = blue, text = "INVADERS")
    start_btn = UIElement(center_position=(500, 550), font_size=30, text_rgb = white, text="PLAY GAME", action=GameState.NEWGAME)
    score_btn = UIElement(center_position=(500, 620), font_size=30, text_rgb = white, text="HIGH SCORES", action=GameState.HIGHSCORE)
    quit_btn = UIElement(center_position=(500, 690), font_size=30, text_rgb = white, text="QUIT", action=GameState.QUIT)
    buttons = RenderUpdates(start_btn, score_btn, quit_btn, title_3, title_4, title_5, title_6)
    return game_loop(screen, buttons)

def highscore(file_name):
    scores = get_highscore(file_name)
    title =  UIPlain(center_position = (500, 200), font_size = 50, text_rgb = white, text = "Highscores")
    first =  UIPlain(center_position = (500, 360), font_size = 30, text_rgb = white, text = '1st: ' + scores.get('high')[0] + ' - ' + scores.get('high')[1])#'1st: ' + scores.get('high')[0])
    second =  UIPlain(center_position = (500, 420), font_size = 30, text_rgb = white, text = '2nd: ' + scores.get('mid')[0] + ' - ' + scores.get('mid')[1])
    third =  UIPlain(center_position = (500, 480), font_size = 30, text_rgb = white, text = '3rd: ' + scores.get('low')[0] + ' - ' + scores.get('low')[1])
    menu_btn = UIElement(center_position=(130, 750), font_size=25, text_rgb = white, text= "Main Menu", action=GameState.TITLE)
    buttons = RenderUpdates(menu_btn, title, first, second, third)
    return game_loop(screen, buttons)

def main():
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        # if game_state == GameState.NEWGAME:
        #     game_state = play()

        # if game_state == GameState.SECOND:
        #     game_state = play_two()

        if game_state == GameState.HIGHSCORE:
            game_state = highscore(highscore_file)

        # if game_state == GameState.DEAD:
        #     game_state = game_over()

        # if game_state == GameState.NAME:
        #     game_state = getting_name()

        if game_state == GameState.QUIT:
            pygame.quit()
            return 0

if __name__ == '__main__':
    main()