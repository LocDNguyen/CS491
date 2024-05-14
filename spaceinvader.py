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
from sounds import *

pygame.init()

highscore_file = 'highscores.txt'

clock = pygame.time.Clock()
sound = Sound('Sounds/menu.wav')

global pause
pause = Pause(True)

rows = 2
cols = 9
alien_cooldown = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders Frontier')
bg = pygame.image.load("Sprites/bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg2 = pygame.image.load("Sprites/background8.png").convert_alpha()
bg2 = pygame.transform.scale(bg2, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg3 = pygame.image.load("Sprites/deadscreen.png").convert_alpha()
bg3 = pygame.transform.scale(bg3, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
            if (key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH):
                self.rect.x += self.speed
                #self.direction = RIGHT
            if key[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
                #self.direction = UP
            if (key[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT):
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
            if not self.ending_part:
                if key[pygame.K_SPACE] and time_now - self.last_shot > self.cooldown:
                    sound.shoot_laser()
                    laser = Laser(self.rect.centerx, self.rect.top)
                    laser_group.add(laser)
                    self.last_shot = time_now
            else:
                if key[pygame.K_SPACE] and time_now - self.last_shot > self.cooldown:
                    sound.shoot_laser()
                    laser = Laser(self.rect.centerx, self.rect.top)
                    laser.damage = round(random.uniform(1, 2))
                    laser_group.add(laser)
                    self.last_shot = time_now
            
            self.mask = pygame.mask.from_surface(self.image)

            self.check_collisions()

        for live in range(self.health_remaining - 1):
           how_much = SCREEN_WIDTH - self.live_image.get_size()[0]
           x = how_much - (live * self.live_image.get_size()[0]) # (-1* (live * (self.live_image.get_size()[0])))
           screen.blit(self.live_image, (x, SCREEN_HEIGHT - self.live_image.get_size()[1]))

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
        collisions2 = pygame.sprite.spritecollide(self, big_boss, True, pygame.sprite.collide_mask)
        if collisions2:
            for alien in collisions2:
                alien.health -= alien.health
            self.health_remaining -= self.health_remaining
        collisions3 = pygame.sprite.spritecollide(self, green_group, True, pygame.sprite.collide_mask)
        if collisions3:
            for alien in collisions3:
                alien.health -= alien.health
            self.health_remaining -= self.health_remaining
        if pygame.sprite.spritecollide(self, rock_group, False, pygame.sprite.collide_mask):
            self.health_remaining -= self.health_remaining
        if pygame.sprite.spritecollide(self, rock_group_two, False, pygame.sprite.collide_mask):
            self.health_remaining -= self.health_remaining
        if self.health_remaining <= 0:
            sound.jet_explosion()
            sound.stop_bg()
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
        self.ending_part = False

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = self.check_laser_image()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.damage = round(random.uniform(0.5, 1), 2)

    def check_collisions(self):
        collisions = pygame.sprite.groupcollide(alien_group, laser_group, False, True, pygame.sprite.collide_mask)
        if collisions and not spaceship.laser2:
            for alien in collisions:
                sound.hit()
                alien.hit = True
                alien.health -= self.damage
                draw_text(alien.rect.x + 70, alien.rect.y + 60, str(self.damage), 25, white, screen)
        collisions2 = pygame.sprite.groupcollide(green_group, laser_group, False, True, pygame.sprite.collide_mask)
        if collisions2 and not spaceship.laser2:
            for alien in collisions2:
                sound.hit()
                alien.hit = True
        elif collisions and spaceship.laser2:
            for alien in collisions:
                alien.health -= 3
        
    def check_boss_collisions(self):
        collisions = pygame.sprite.groupcollide(big_boss, laser_group, False, True, pygame.sprite.collide_mask)
        if collisions and not spaceship.laser2:
            for boss in collisions:
                sound.hit()
                boss.hit = True
                damage = round(random.uniform(1, 3), 2)
                boss.health -= damage
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
        self.rect.y -= 7
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
        self.boss_move_direction = 0
        self.move_down = 2
        self.green_move_down = 0
        self.health = health
        self.alive = True
        self.hit = False
        self.blue_move_down = False
        self.type = type
        self.sprites = AlienSprites(self)

    def update(self, dt):
        self.sprites.update(dt)
        if self.type == 'blue' and not self.blue_move_down:
            if self.alive:
                self.rect.x += self.move_direction
                if self.health <= 0:
                    spaceship.score += 100
                    self.alive = False
            else:
                sound.alien_explosion()
                if self.sprites.animations[2].finished:
                    self.kill()
        if self.type == 'blue' and self.blue_move_down:
            if self.alive:
                self.rect.y += 0.6
                if self.health <= 0:
                    spaceship.score += 100
                    self.alive = False
                if self.rect.bottom > SCREEN_HEIGHT + 90:
                    spaceship.health_remaining -= 10
                    spaceship.score -= 10000000
                    self.alive = False
            else:
                sound.alien_explosion()
                if self.sprites.animations[2].finished:
                    self.kill()
        if self.type == 'pink':
            if self.alive:
                if self.rect.x < spaceship.rect.x:
                    self.rect.x += 2
                if self.rect.x > spaceship.rect.x:
                    self.rect.x -= 2
                if self.rect.y < spaceship.rect.y:
                    self.rect.y += 2
                if self.rect.y > spaceship.rect.y:
                    self.rect.y -= 2
                if self.health <= 0:
                    spaceship.score += 100
                    self.alive = False
            else:
                sound.alien_explosion()
                if self.sprites.animations[2].finished:
                    self.kill()
        if self.type == 'red':
            if self.alive:
                self.rect.y += self.move_down
                self.rect.x += self.boss_move_direction
                if self.rect.bottom > SCREEN_HEIGHT + 90:
                    spaceship.health_remaining -= 10
                    spaceship.score -= 10000000
                    self.alive = False
                if self.health <= 0:
                    spaceship.score += 100000
                    self.alive = False
            else:
                sound.alien_explosion()
                if self.sprites.animations[2].finished:
                    self.kill()
        if self.type == 'green':
            if self.alive:
                self.rect.y += self.green_move_down
                if self.health <= 0:
                    spaceship.score += 1
                    self.alive = False
            else:
                sound.alien_explosion()
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
        if self.rect.bottom > SCREEN_HEIGHT + 75:
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
        self.alien = alien
        if self.orientation:
            self.image = pygame.image.load("Sprites/red_alien_shot.png").convert_alpha()
            #self.image = pygame.transform.scale(self.image, (32, 32))
            self.image = pygame.transform.rotate(self.image, 180)
        else:
            self.image = pygame.image.load("Sprites/red_alien_shot.png").convert_alpha()
            #self.image = pygame.transform.scale(self.image, (32, 32))
            self.image = pygame.transform.rotate(self.image, 90)
        if self.alien != None:
            self.type = alien.type
            if self.type == 'green':
                self.image = pygame.image.load("Sprites/green_alien_shot.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, dt):
        if self.alien == None or self.type != 'green':
            if self.orientation:
                self.rect.y += 4
            else:
                self.rect.x -= 4
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()
            if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
                self.kill()
                sound.hit()
                spaceship.direction = HIT
                spaceship.health_remaining -= 1
            if pygame.sprite.spritecollide(self, rock_group, False, pygame.sprite.collide_mask):
                self.kill()
            if pygame.sprite.spritecollide(self, rock_group_two, False, pygame.sprite.collide_mask):
                self.kill()
        else:
            if self.rect.x < spaceship.rect.x:
                self.rect.x += 4
            if self.rect.x > spaceship.rect.x:
                self.rect.x -= 4
            if self.rect.y < spaceship.rect.y:
                self.rect.y += 4
            if self.rect.y > spaceship.rect.y:
                self.rect.y -= 4
            if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
                self.kill()
                sound.hit()
                spaceship.direction = HIT
                spaceship.health_remaining -= 1
            collisions = pygame.sprite.groupcollide(green_group, alien_laser_group, False, True, pygame.sprite.collide_mask)
            if collisions and not spaceship.laser2:
                for alien in collisions:
                    sound.hit()
                    alien.hit = True
                    damage = round(random.uniform(0.1, 1), 2)
                    alien.health -= damage
                    draw_text(alien.rect.x + 70, alien.rect.y + 60, str(damage), 25, white, screen)

class Big_Alien_Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/red_alien_shot.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32*12, 32*12))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, dt):
        self.rect.y += 4
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            sound.hit()
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
green_group = pygame.sprite.Group()

spaceship = Spaceship(CENTER, SCREEN_HEIGHT - 100, 3)
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

def show_score():
    font = pygame.font.SysFont('freesansbold.ttf', 37)
    score = font.render("Score : " + str(spaceship.score), True, white)
    screen.blit(score, (1, 775))

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
    green_group.draw(screen)


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
                if ui_action == GameState.NEWGAME:
                    sound.start_button()
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
    big_boss_movement_timer = pygame.time.get_ticks()
    create_aliens()
    pressedEscToBegin = True
    pausedText = False
    alternate = True
    stop = 0
    move = 0
    move_on = 10
    stop_making = 0
    start_making_pink = 0
    start_making_green = 0
    numOfPinkSpawned = 0
    once = True
    list_for_x_y_of_pink_alien = [(SCREEN_WIDTH + 50, 50), (SCREEN_WIDTH + 50, 100), (SCREEN_WIDTH + 50, 200), (SCREEN_WIDTH + 50, 300), 
                                  (-50, 50), (-50, 100), (-50, 200), (-50, 300),
                                  (50, -50), (100, -50), (200, -50), (300, -50),
                                  (50, SCREEN_HEIGHT + 50), (100, SCREEN_HEIGHT + 50), (200, SCREEN_HEIGHT + 50), (300, SCREEN_HEIGHT + 50),]
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
                        if once:
                            sound.begin()
                            once = False
                        sound.undeafen()
                        showSprites()
                        pausedText = False
                    else:
                        sound.pause_button()
                        sound.deafen()
                        pausedText = True

            if event.type == pygame.QUIT:
                run = False

        if pressedEscToBegin:
            draw_text(CENTER, 450, "Press Escape to Begin", 37, white, screen)
        if pausedText:
            draw_text(CENTER, 450, "Paused", 37, white, screen)

        if not pause.paused:
            #Eliminate all blue aliens
            if start_making_pink == 0 and start_making_green == 0 and stop == 0:
                if time_now - last_alien_shot > alien_cooldown and len(alien_laser_group) < 5 and len(alien_group) > 0:
                    sound.shoot_laser()
                    shooting_alien = random.choice(alien_group.sprites())
                    alien_laser = Alien_Laser(shooting_alien.rect.centerx, shooting_alien.rect.bottom, True, shooting_alien)
                    alien_laser_group.add(alien_laser)
                    last_alien_shot = time_now

            #Homing enemies
            #Spawn them outside screen
            #Spawm them in intervals at random coordinates
            #Have a counter to count how many enemies have died in order to stop mech
            #Eliminate all pink aliens
            if len(alien_group) == 0 and stop == 0:
                start_making_pink = 1
            if start_making_pink == 1:
                if time_now - end_timer_for_spawning_pink_aliens > 1000:
                    spawn = random.choice(list_for_x_y_of_pink_alien)
                    alien = Alien(spawn[0], spawn[1], 0.1, 'pink')
                    alien_group.add(alien)
                    end_timer_for_spawning_pink_aliens = time_now
                    numOfPinkSpawned += 1
                if numOfPinkSpawned == 15:
                    start_making_pink += 1
                    stop += 1

            #Eliminate all green aliens
            if len(alien_group) == 0 and stop == 1 and start_making_green == 0:
                start_making_green = 1
            if start_making_green == 1:
                alien = Alien(250, -100, 1, "green")
                alien1 = Alien(750, -100, 1, "green")
                alien2 = Alien(250, -300, 1, "green")
                alien3 = Alien(750, -300, 1, "green")
                green_group.add(alien)
                green_group.add(alien1)
                green_group.add(alien2)
                green_group.add(alien3)
                first_green = green_group.sprites()[0]
                start_making_green += 1
            if start_making_green == 2:
                if first_green.rect.bottom != 400:
                    for alien in green_group:
                        alien.green_move_down = 3
                else:
                    for alien in green_group:
                        alien.green_move_down = 0
                    start_making_green += 1
            if start_making_green == 3:
                if len(alien_laser_group) != 1 and len(green_group) > 0:
                    green_shooting_alien = random.choice(green_group.sprites())
                    if spaceship.rect.x <= green_shooting_alien.rect.x and spaceship.rect.y <= green_shooting_alien.rect.y:
                        alien_laser = Alien_Laser(green_shooting_alien.rect.left, green_shooting_alien.rect.top, True, green_shooting_alien)
                    elif spaceship.rect.x >= green_shooting_alien.rect.x and spaceship.rect.y >= green_shooting_alien.rect.y:
                        alien_laser = Alien_Laser(green_shooting_alien.rect.right, green_shooting_alien.rect.bottom, True, green_shooting_alien)
                    elif spaceship.rect.x >= green_shooting_alien.rect.x and spaceship.rect.y <= green_shooting_alien.rect.y:
                        alien_laser = Alien_Laser(green_shooting_alien.rect.right, green_shooting_alien.rect.top, True, green_shooting_alien)
                    elif spaceship.rect.x <= green_shooting_alien.rect.x and spaceship.rect.y >= green_shooting_alien.rect.y:
                        alien_laser = Alien_Laser(green_shooting_alien.rect.left, green_shooting_alien.rect.bottom, True, green_shooting_alien)
                    alien_laser_group.add(alien_laser)
                if len(green_group) == 0:
                    alien_laser_group.empty()
                    start_making_green += 1
            if len(alien_group) == 0 and len(green_group) == 0 and len(alien_laser_group) == 0 and start_making_green == 4:
                start_making_green += 1
                stop += 1

            #First hide behind rock mech
            if len(alien_group) == 0 and len(rock_group) == 0 and stop == 2:
                rockCover = Rock_Hori(SCREEN_WIDTH + 40, 500)
                rock_group.add(rockCover)
            elif len(rock_group) == 1 and stop == 2:
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

            #Second hide behind rock mech
            if stop == 3 and len(rock_group) == 0 and len(rock_group_two) == 0 and len(alien_group) == 0:
                rockCover = Rock_Vert(700, SCREEN_HEIGHT + 40)
                rock_group_two.add(rockCover)
            elif stop == 3 and len(rock_group_two) == 1:
                if time_now - end_timer_for_first_laser_mech > 200:
                    for row in range(1):
                        for item in range(40):
                            # Enemy(buffer to the left + pixels apart, buffer at the top + pixels apart)
                            laser = Alien_Laser((SCREEN_WIDTH + row * 20), (2 + item * 50), False, None)
                            all_enemy_lasers.add(laser)
                    end_timer_for_first_laser_mech = time_now
                if rockCover.rect.top < 250:
                    stop += 1

            #Dodge falling laser mech
            if stop == 4 and len(rock_group_two) == 0:
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
            if stop == 5 and len(alien_group) == 0 and len(falling_lasers) == 0:
                sound.boss_battle()
                boss = Alien(SCREEN_WIDTH / 2 - 35, -100, 5, "red")
                big_boss.add(boss)
                stop += 1
                spawn = True

            if stop == 6:
                if len(big_boss) == 1:
                    for boss in big_boss:
                        if boss.rect.bottom == 100 and move == 0:
                            boss.move_down = 0
                            boss.boss_move_direction = 1
                            move += 1
                        if move == 1:
                            if time_now - big_boss_movement_timer > 5000:
                                if boss.boss_move_direction > 0:
                                    boss.boss_move_direction = random.randint(1, 5)
                                else:
                                    boss_speed_change = random.randint(1, 5)
                                    boss_speed_change *= -1
                                    boss.boss_move_direction = boss_speed_change
                                big_boss_movement_timer = time_now
                            if boss.check_edges():
                                boss.boss_move_direction *= -1
                            if stop_making == 0:
                                for row in range(1):
                                    for item in range(20):
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
            
            #Endless
            if stop == 7 and len(alien_laser_group) == 0:
                sound.ending()
                spaceship.cooldown = 200
                spaceship.ending_part = True
                number_of_rows = 1
                stop += 1
            if stop == 8:
                if len(alien_group) == 0:
                    for row in range(number_of_rows):
                        for col in range(9):
                            alien = Alien(100 + col * 100, -1*(row * 70), 2, 'blue')
                            alien.blue_move_down = True
                            alien.move_direction = 0.4
                            alien_group.add(alien)
                        number_of_rows += 1

            laser_group.update()
            alien_group.update(dt)
            alien_laser_group.update(dt)
            all_enemy_lasers.update(dt)
            rock_group.update()
            rock_group_two.update()
            falling_lasers.update(dt)
            big_boss.update(dt)
            green_group.update(dt)

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
        show_score()

        pygame.display.update()
    return GameState.QUIT

def getting_name():
    user_text = ''
    global highscore_file
    font = pygame.font.SysFont('freesansbold.ttf', 37)
    input_rect = pygame.Rect(465, 720, 58, 35)
    global pause 
    pause = Pause(True)

    running = True
    while running:

        screen.blit(bg3, (0, 0))

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
                if len(user_text) > 0 and len(user_text) < 3:
                    sound.key_click()
                if event.key == pygame.K_RETURN:
                    set_highscore(highscore_file, user_text, spaceship.score)
                    return GameState.DEAD

        # Displaying what the user types in
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        text = font.render(user_text, True, WHITE)
        screen.blit(text, (input_rect.x + 5, input_rect.y + 5))

        # Box around the user input moves with the input
        input_rect.w = max(10, text.get_width() + 10)

        pygame.display.update()  # update our screen
        # clock.tick(fps)

def main():
    game_state = GameState.TITLE
    once = True

    while True:
        screen.blit(bg, (0, 0))
        if once:
            sound2 = Sound('Sounds/menu2.wav')
            sound2.play_bg()
            once = False

        if game_state == GameState.TITLE:
            sound.stop_sound()
            game_state = title_screen(screen, CENTER, game_loop)

        if game_state == GameState.NEWGAME:
            sound.fade_bg()
            time.sleep(0.7)
            game_state = play()

        if game_state == GameState.HIGHSCORE:
            game_state = highscore(screen, highscore_file, CENTER, game_loop)

        if game_state == GameState.DEAD:
            once = True
            game_state = game_over(screen, SCREEN_HEIGHT, CENTER, game_loop, spaceship, spaceship_group, 
                                   laser_group, alien_group, alien_laser_group, rock_group, rock_group_two,
                                   all_enemy_lasers, alien_still_group, falling_lasers, big_boss, green_group, sound)
            
        if game_state == GameState.NAME:
            game_state = getting_name()

        if game_state == GameState.QUIT:
            pygame.quit()
            return 0

if __name__ == '__main__':
    main()