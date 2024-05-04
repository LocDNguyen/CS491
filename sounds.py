import pygame as pg
import time


class Sound:
    def __init__(self, sound):
        pg.mixer.init()
        if sound != None:
            pg.mixer.music.load(sound)
        pg.mixer.music.set_volume(0.1)
        laser_sound = pg.mixer.Sound('Sounds/shoot.wav')
        laser_sound.set_volume(0.1)
        start_sound = pg.mixer.Sound('Sounds/start.wav')
        start_sound.set_volume(0.2)
        explosion_sound = pg.mixer.Sound('Sounds/explosion.wav')
        explosion_sound.set_volume(0.1)
        hover_over = pg.mixer.Sound('Sounds/hover_over2.wav')
        pause_sound = pg.mixer.Sound('Sounds/pause2.wav')
        pause_sound.set_volume(0.2)
        game_over_sound = pg.mixer.Sound('Sounds/game_over.wav')
        game_over_sound.set_volume(0.1)
        key_click_sound = pg.mixer.Sound('Sounds/key_click.wav')
        explode_sound = pg.mixer.Sound('Sounds/explode.wav')
        explode_sound.set_volume(0.1)
        hit_sound = pg.mixer.Sound('Sounds/hit.wav')
        hit_sound.set_volume(0.1)
        self.once = True
        self.sounds = {'start': start_sound, 'hover': hover_over, 'pause': pause_sound, 
                       'laser': laser_sound, 'explosion': explosion_sound, 'over': game_over_sound,
                       'key': key_click_sound, 'explode': explode_sound, 'hit': hit_sound}

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def fade_bg(self):
        pg.mixer.music.fadeout(10)

    def shoot_laser(self): pg.mixer.Sound.play(self.sounds['laser'])
    def big_alien_move(self): pg.mixer.Sound.play(self.sounds['alien'])
    def big_alien_stop(self): pg.mixer.Sound.stop(self.sounds['alien'])
    def start_button(self): pg.mixer.Sound.play(self.sounds['start'])
    def hover_button(self): pg.mixer.Sound.play(self.sounds['hover'])
    def pause_button(self): pg.mixer.Sound.play(self.sounds['pause'])
    def jet_explosion(self): pg.mixer.Sound.play(self.sounds['explosion'])
    def game_over(self): pg.mixer.Sound.play(self.sounds['over'])
    def key_click(self): pg.mixer.Sound.play(self.sounds['key'])
    def alien_explosion(self): pg.mixer.Sound.play(self.sounds['explode'])
    def hit(self): pg.mixer.Sound.play(self.sounds['hit'])

    # def gameover(self):
    #     if self.once:
    #         pg.mixer.music.load('Sounds/game_over.wav')
    #         self.play_bg()
    #         time.sleep(3.4)
    #         self.stop_bg()
    #         self.once = False

    def begin(self):
        pg.mixer.music.load('Sounds/begin2.wav')
        pg.mixer.music.set_volume(0.1)
        self.play_bg()

    def boss_battle(self):
        self.stop_bg()
        pg.mixer.music.load('Sounds/boss.wav')
        pg.mixer.music.set_volume(0.1)
        self.play_bg()

    def ending(self):
        self.stop_bg()
        pg.mixer.music.load('Sounds/end.wav')
        pg.mixer.music.set_volume(0.1)
        self.play_bg()
    # def speedup(self):
    #     self.stop_bg()
    #     pg.mixer.music.load('sounds/startrek_speed.wav')
    #     self.play_bg()

    # def speedup2(self):
    #     self.stop_bg()
    #     pg.mixer.music.load('sounds/startrek_speed_two.wav')
    #     self.play_bg()

    def deafen(self):
        pg.mixer.music.set_volume(0)

    def undeafen(self):
        pg.mixer.music.set_volume(0.1)

    def stop_sound(self):
        pg.mixer.Sound.stop(self.sounds['over'])