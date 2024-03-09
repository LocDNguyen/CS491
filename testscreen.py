from pygame.sprite import RenderUpdates
from buttons import UIPlain, UIElement
from highscore import get_highscore
from gamestate import GameState

white = (255, 255, 255)
green = (255, 0, 255)
red = (255, 0, 0)
blue = (0, 255, 255)

def title_screen(screen, center, game_loop):
    title_1 =  UIPlain(center_position = (center, 160), font_size = 110, text_rgb = white, text = "SPACE INVADERS")
    title_2 =  UIPlain(center_position = (center, 290), font_size = 110, text_rgb = white, text = "FRONTIER")
    title_3 =  UIPlain(center_position = (center + 10, 170), font_size = 110, text_rgb = blue, text = "SPACE INVADERS")
    title_4 =  UIPlain(center_position = (center + 10, 300), font_size = 110, text_rgb = blue, text = "FRONTIER")
    start_btn = UIElement(center_position = (center, 550), font_size = 30, text_rgb = white, text = "PLAY GAME", action=GameState.NEWGAME)
    score_btn = UIElement(center_position = (center, 620), font_size = 30, text_rgb = white, text = "HIGH SCORES", action=GameState.HIGHSCORE)
    quit_btn = UIElement(center_position = (center, 690), font_size = 30, text_rgb = white, text = "QUIT", action=GameState.QUIT)
    buttons = RenderUpdates(start_btn, score_btn, quit_btn, title_1, title_2, title_3, title_4)
    return game_loop(screen, buttons)

def highscore(screen, file_name, center, game_loop):
    scores = get_highscore(file_name)
    title =  UIPlain(center_position = (center, 200), font_size = 50, text_rgb = white, text = "Highscores")
    first =  UIPlain(center_position = (center, 360), font_size = 30, text_rgb = white, text = '1st: ' + scores.get('high')[0] + ' - ' + scores.get('high')[1])#'1st: ' + scores.get('high')[0])
    second =  UIPlain(center_position = (center, 420), font_size = 30, text_rgb = white, text = '2nd: ' + scores.get('mid')[0] + ' - ' + scores.get('mid')[1])
    third =  UIPlain(center_position = (center, 480), font_size = 30, text_rgb = white, text = '3rd: ' + scores.get('low')[0] + ' - ' + scores.get('low')[1])
    menu_btn = UIElement(center_position = (130, 750), font_size = 25, text_rgb = white, text = "Main Menu", action=GameState.TITLE)
    buttons = RenderUpdates(menu_btn, title, first, second, third)
    return game_loop(screen, buttons)

def game_over(screen, screen_height, center, game_loop, spaceship, spaceship_group, laser_group, alien_group, alien_laser_group):
    game_over = UIPlain(center_position=(center, 200), font_size=70, text_rgb=white, text="GAME OVER")
    final_score = UIPlain(center_position=(center, 300), font_size=30, text_rgb=white, text="Final Score : " + str(spaceship.score))
    retry_btn = UIElement(center_position=(center, 400), font_size=30, text_rgb=white, text="Restart", action=GameState.NEWGAME)
    menu_btn = UIElement(center_position=(center, 650), font_size=30, text_rgb=white, text="Main Menu", action=GameState.TITLE)
    quit_btn = UIElement(center_position=(center, 700), font_size=30, text_rgb=white, text="Quit", action=GameState.QUIT)

    spaceship_group.empty()
    laser_group.empty()
    alien_group.empty()
    alien_laser_group.empty()
    # rock_group.empty()
    # rock_group_two.empty()
    # all_enemies_lasers.empty()
    # alien_still_group.empty()
    # powerup_group.empty()
    # big_boss_group.empty()
    spaceship.reset(center, screen_height - 100, 3)
    spaceship_group.add(spaceship)

    buttons = RenderUpdates(game_over, final_score, retry_btn, menu_btn, quit_btn)
    return game_loop(screen, buttons)