#!/usr/bin/env python3

import pygame
from pygame.locals import *
import random

from buttons import draw_text
from gamestate import GameState
from highscore import set_highscore
from testscreen import title_screen, highscore, game_over, white
from sprites import PlayerSprite, AlienSprites
from constants import *
from pause import *

pygame.init()

highscore_file = 'highscores.txt'

screen_width = 1000
screen_height = 800
center = screen_width / 2

clock = pygame.time.Clock()

pause = Pause(True)

rows = 1#3
cols = 1#7
alien_cooldown = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders Frontier')
bg = pygame.Surface(screen.get_size())
bg.fill((0, 0, 0))
bg2 = pygame.image.load("Sprites/background8.png").convert_alpha()
bg2 = pygame.transform.scale(bg2, (screen_width, screen_height))

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)

        self.reset(x, y, health)

    def update(self, dt):
        self.sprites.update(dt)
        if self.alive:
            key = pygame.key.get_pressed()
            self.direction = self.getKey()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
                #self.direction = LEFT
            if (key[pygame.K_RIGHT] and self.rect.right < screen_width):
                self.rect.x += self.speed
                #self.direction = RIGHT
            if key[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
                #self.direction = UP
            if (key[pygame.K_DOWN] and self.rect.bottom < screen_height):
                self.rect.y += self.speed
                #self.direction = DOWN
            # if (key[pygame.K_UP] and key[pygame.K_LEFT]):
            #     self.direction = LEFTUP
            # if (key[pygame.K_DOWN] and key[pygame.K_LEFT]):
            #     self.direction = LEFTDOWN
            # if (key[pygame.K_UP] and key[pygame.K_RIGHT]):
            #     self.direction = RIGHTUP
            # if (key[pygame.K_DOWN] and key[pygame.K_RIGHT]):
            #     self.direction = RIGHTDOWN

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

        #pygame.draw.rect(self.image, RED, [0, 0, self.rect.x, self.rect.y], 1)

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
        if key_pressed[K_UP] and key_pressed[K_LEFT]:
            return LEFTUP
        return STOP
    
    def check_collisions(self):
        collisions = pygame.sprite.spritecollide(self, alien_group, True, pygame.sprite.collide_mask)
        if collisions:
            for alien in collisions:
                alien.health -= alien.health
            self.health_remaining -= self.health_remaining
        if pygame.sprite.spritecollide(self, rock_group, False, pygame.sprite.collide_mask):
            self.health_remaining -= self.health_remaining
        if pygame.sprite.spritecollide(self, rock_group_two, False, pygame.sprite.collide_mask):
            self.health_remaining -= self.health_remaining
        if self.health_remaining <= 0:
            pause.setPause(pauseTime = 5.5, func = GameState.NAME)
            spaceship.alive = False
        
        

    def reset(self, x, y, health):
        self.image = pygame.image.load("Sprites/jetv2.png").convert_alpha()
        self.live_image = pygame.transform.rotozoom(self.image, 0, 0.7)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.speed = 8
        self.cooldown = 400
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
        self.damage = 0

    def check_collisions(self):
        collisions = pygame.sprite.groupcollide(alien_group, laser_group, False, True, pygame.sprite.collide_mask)
        if collisions and not spaceship.laser2:
            for alien in collisions:
                alien.hit = True
                damage = round(random.uniform(0.1, 1), 2)
                alien.health -= damage
                draw_text(alien.rect.x + 70, alien.rect.y + 60, str(damage), 25, white, screen)
        elif collisions and spaceship.laser2:
            for alien in collisions:
                alien.health -= 3
        
    def check_boss_collisions(self):
        collisions = pygame.sprite.groupcollide(big_boss, laser_group, False, True, pygame.sprite.collide_mask)
        if collisions and not spaceship.laser2:
            for boss in collisions:
                boss.health -= 1
        elif collisions and spaceship.laser2:
            for boss in collisions:
                boss.health -= 3

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
        self.check_boss_collisions()


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, health, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/jet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.move_counter = 0
        self.move_direction = 1
        self.health = health
        self.alive = True
        self.hit = False
        self.type = type
        self.sprites = AlienSprites(self)

    def update(self, dt):
        self.sprites.update(dt)
        if self.type == 'blue':
            if self.alive:
                self.rect.x += self.move_direction
                if self.health <= 0:
                    spaceship.score += 100
                    self.alive = False
            else:
                if self.sprites.animations[2].finished:
                    self.kill()
        if self.type == 'pink':
            if self.alive:
                if self.rect.x < spaceship.rect.x:
                    self.rect.x += 1
                if self.rect.x > spaceship.rect.x:
                    self.rect.x -= 1
                if self.rect.y < spaceship.rect.y:
                    self.rect.y += 1
                if self.rect.y > spaceship.rect.y:
                    self.rect.y -= 1
                if self.health <= 0:
                    spaceship.score += 100
                    self.alive = False
            else:
                if self.sprites.animations[2].finished:
                    self.kill()
            
    def change_direction(self):
        for alien in alien_group:
            alien.rect.y += 8
            alien.move_direction *= -1

    def check_edges(self):
        screen_rect = screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    
class Alien_Still(pygame.sprite.Sprite):
    def __init__(self, x, y, type):

        super().__init__()
        # Draw the enemy
        self.image = pygame.image.load("Sprites/jet.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.type = type

class Big_Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/red_alien1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (700, 200))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_down = 2
        self.move_direction = 0
        self.health = health

    def update(self, dt):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y += self.move_down
        self.rect.x += self.move_direction
        if self.rect.bottom > screen_height + 75:
            spaceship.health_remaining -= 10
            spaceship.score -= 10000000
            self.kill()
        if self.health <= 0:
            spaceship.score += 100000
            self.kill()

    def check_edges(self):
        screen_rect = screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    
class Alien_Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation, alien):
        pygame.sprite.Sprite.__init__(self)
        self.orientation = orientation
        self.type = alien
        if self.orientation:
            self.image = pygame.image.load("Sprites/sprite_0.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.image = pygame.transform.rotate(self.image, 180)
        else:
            self.image = pygame.image.load("Sprites/sprite_0.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, dt):
        if self.orientation:
            self.rect.y += 4
        else:
            self.rect.x -= 4
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.direction = HIT
            spaceship.health_remaining -= 1
        if pygame.sprite.spritecollide(self, rock_group, False, pygame.sprite.collide_mask):
            self.kill()
        if pygame.sprite.spritecollide(self, rock_group_two, False, pygame.sprite.collide_mask):
            self.kill()

class Big_Alien_Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/sprite_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, dt):
        self.rect.y += 4
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.health_remaining -= 10

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


spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_laser_group = pygame.sprite.Group()
rock_group = pygame.sprite.Group()
rock_group_two = pygame.sprite.Group()
all_enemy_lasers = pygame.sprite.Group()
alien_still_group = pygame.sprite.Group()
falling_lasers = pygame.sprite.Group()
big_boss = pygame.sprite.Group()

spaceship = Spaceship(center, screen_height - 100, 99)
spaceship_group.add(spaceship)


def create_aliens():
        for row in range(rows):
            for col in range(cols):
                alien = Alien(100 + col * 100, 100 + row * 70, 2, 'blue')
                alien_group.add(alien)
            
def edge_check():
    for alien in alien_group:
        if alien.type == 'blue':
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
    big_boss.draw(screen)


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
    last_big_shot = pygame.time.get_ticks()
    end_timer_for_first_laser_mech = pygame.time.get_ticks()
    ender_timer = pygame.time.get_ticks()
    end_timer_for_spawning_pink_aliens = pygame.time.get_ticks()
    create_aliens()
    pressedEscToBegin = True
    pausedText = False
    alternate = True
    stop = 0
    move = 0
    move_on = 10
    stop_making = 0
    start_making_pink = 0
    numOfPinkSpawned = 0
    list_for_x_y_of_pink_alien = [(screen_width + 50, 50), (screen_width + 50, 100), (screen_width + 50, 200), (screen_width + 50, 300), 
                                  (-50, 50), (-50, 100), (-50, 200), (-50, 300),
                                  (50, -50), (100, -50), (200, -50), (300, -50),
                                  (50, screen_height + 50), (100, screen_height + 50), (200, screen_height + 50), (300, screen_height + 50),]
    while run:
        dt = clock.tick(60) / 500.0
        time_now = pygame.time.get_ticks()
        screen.blit(bg2, (0, 0))

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
            draw_text(screen_width / 2, 450, "Press Escape to Begin", 37, white, screen)
        if pausedText:
            draw_text(screen_width / 2, 450, "Paused", 37, white, screen)

        if not pause.paused:
            if start_making_pink == 0:
                if time_now - last_alien_shot > alien_cooldown and len(alien_laser_group) < 5 and len(alien_group) > 0:
                    shooting_alien = random.choice(alien_group.sprites())
                    alien_laser = Alien_Laser(shooting_alien.rect.centerx, shooting_alien.rect.bottom, True, shooting_alien)
                    alien_laser_group.add(alien_laser)
                    last_alien_shot = time_now

            #Homing enemies
            #Spawn them outside screen
            #Spawm them in intervals at random coordinates
            #Have a counter to count how many enemies have died in order to stop mech
            if len(alien_group) == 0 and stop == 0:
                start_making_pink = 1
            if start_making_pink == 1:
                if time_now - end_timer_for_spawning_pink_aliens > 1000:
                    spawn = random.choice(list_for_x_y_of_pink_alien)
                    alien = Alien(spawn[0], spawn[1], 0.1, 'pink')
                    alien_group.add(alien)
                    end_timer_for_spawning_pink_aliens = time_now
                    numOfPinkSpawned += 1
                if numOfPinkSpawned == 20:
                    start_making_pink += 1
                    stop += 1

            #First Mech
            if len(alien_group) == 0 and len(rock_group) == 0 and stop == 1:
                rockCover = Rock_Hori(screen_width + 40, 500)
                rock_group.add(rockCover)
            elif len(rock_group) == 1 and stop == 1:
                if time_now - end_timer_for_first_laser_mech > 800:
                    if alternate:
                        for row in range(1):
                            for item in range(50):
                                # Enemy(buffer to the left + pixels apart, buffer at the top + pixels apart)
                                laser = Alien_Laser((10 + item * 20), (2 + row * 50), True, None)
                                all_enemy_lasers.add(laser)
                        alternate = False
                    else:
                        for row in range(1):
                            for item in range(50):
                                # Enemy(buffer to the left + pixels apart, buffer at the top + pixels apart)
                                laser = Alien_Laser((10 + item * 20), (2 + row * 50), True, None)
                                all_enemy_lasers.add(laser)
                        alternate = True
                    end_timer_for_first_laser_mech = time_now
                if rockCover.rect.left < 250:
                    stop += 1

            #Second Mech
            if stop == 2 and len(rock_group) == 0 and len(rock_group_two) == 0 and len(alien_group) == 0:
                rockCover = Rock_Vert(700, screen_height + 40)
                rock_group_two.add(rockCover)
            elif stop == 2 and len(rock_group_two) == 1:
                if time_now - end_timer_for_first_laser_mech > 200:
                    for row in range(1):
                        for item in range(40):
                            # Enemy(buffer to the left + pixels apart, buffer at the top + pixels apart)
                            laser = Alien_Laser((screen_width + row * 20), (2 + item * 50), False, None)
                            all_enemy_lasers.add(laser)
                    end_timer_for_first_laser_mech = time_now
                if rockCover.rect.top < 250:
                    stop += 1

            #Third Mech
            if stop == 3 and len(rock_group_two) == 0:
                if time_now - end_timer_for_first_laser_mech > 70:
                    if stop_making == 0:
                        for row in range(1):
                            for item in range(50):
                                # Enemy(buffer to the left + pixels apart, buffer at the top + pixels apart)
                                enemy = Alien_Still((10 + item * 20), (-20 + row * 50), None)
                                alien_still_group.add(enemy)
                            stop_making = 1
                    if time_now - last_alien_shot > alien_cooldown and len(falling_lasers) < 200:
                        attacking_enemy = random.choice(alien_still_group.sprites())
                        enemy_laser = Alien_Laser(attacking_enemy.rect.centerx, attacking_enemy.rect.bottom, True, None)
                        falling_lasers.add(enemy_laser)
                        end_timer_for_first_laser_mech = time_now
                if move_on > 0:
                    if time_now - ender_timer > 2000:
                        move_on -= 1
                        ender_timer = time_now
                if move_on == 0:
                    alien_still_group.empty()
                    stop_making = 0
                    stop += 1

            #Big Boss Mech
            if stop == 4 and len(alien_group) == 0:
                boss = Big_Boss(screen_width / 2, -300, 5)
                big_boss.add(boss)
                stop += 1
                spawn = True

            if stop == 5:
                if len(big_boss) == 1:
                    for boss in big_boss:
                        if boss.rect.bottom == 200 and move == 0:
                            boss.move_down = 0
                            boss.move_direction = 1
                            move += 1
                        if move == 1:
                            if boss.check_edges():
                                boss.move_direction *= -1
                            if stop_making == 0:
                                for row in range(1):
                                    for item in range(13):
                                        # Enemy(buffer to the left + pixels apart, buffer at the top + pixels apart)
                                        enemy = Alien_Still((30 + item * 60), (40 + row * 70), None)
                                        alien_still_group.add(enemy)
                                    stop_making = 1
                            if time_now - last_big_shot > 1000:
                                for ele in range(len(alien_still_group)):
                                    if ele != len(alien_still_group) - 1:
                                        attacking_enemy = random.choice(alien_still_group.sprites())
                                        enemy_laser = Alien_Laser(attacking_enemy.rect.centerx, attacking_enemy.rect.bottom, True, None)
                                        all_enemy_lasers.add(enemy_laser)
                                shooting_alien = random.choice(big_boss.sprites())
                                alien_laser = Big_Alien_Laser(shooting_alien.rect.centerx - 105, shooting_alien.rect.bottom - 270)
                                alien_laser2 = Big_Alien_Laser(shooting_alien.rect.centerx - 195, shooting_alien.rect.bottom - 300)
                                alien_laser3 = Big_Alien_Laser(shooting_alien.rect.centerx - 285, shooting_alien.rect.bottom - 330)
                                alien_laser4 = Big_Alien_Laser(shooting_alien.rect.centerx + 170, shooting_alien.rect.bottom - 270)
                                alien_laser5 = Big_Alien_Laser(shooting_alien.rect.centerx + 260, shooting_alien.rect.bottom - 300)
                                alien_laser6 = Big_Alien_Laser(shooting_alien.rect.centerx + 350, shooting_alien.rect.bottom - 330)
                                list = [alien_laser, alien_laser2, alien_laser3, alien_laser4, alien_laser5, alien_laser6]
                                shooting = random.choice(list)
                                alien_laser_group.add(shooting)
                                last_big_shot = time_now
                else:
                    alien_still_group.empty()
                    stop += 1

            laser_group.update()
            alien_group.update(dt)
            alien_laser_group.update(dt)
            all_enemy_lasers.update(dt)
            rock_group.update()
            rock_group_two.update()
            falling_lasers.update(dt)
            big_boss.update(dt)

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