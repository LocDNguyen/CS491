# import pygame
# from constants import *

# # class Player():
# #     def __init__(self, x, y, width, height, color):
# #         self.x = x
# #         self.y = y
# #         self.width = width
# #         self.height = height
# #         self.color = color
# #         self.rect = (x,y,width,height)
# #         self.vel = 3

# #     def draw(self, win):
# #         pygame.draw.rect(win, self.color, self.rect)

# #     def move(self):
# #         keys = pygame.key.get_pressed()

# #         if keys[pygame.K_LEFT]:
# #             self.x -= self.vel

# #         if keys[pygame.K_RIGHT]:
# #             self.x += self.vel

# #         if keys[pygame.K_UP]:
# #             self.y -= self.vel

# #         if keys[pygame.K_DOWN]:
# #             self.y += self.vel

# #         self.update()

# #     def update(self):
# #         self.rect = (self.x, self.y, self.width, self.height)

# class Spaceship(pygame.sprite.Sprite):
#     def __init__(self, x, y, health):
#         pygame.sprite.Sprite.__init__(self)

#         self.reset(x, y, health)

#     def update(self):
#         if self.alive:
#             key = pygame.key.get_pressed()
#             if key[pygame.K_LEFT] and self.rect.left > 0:
#                 self.rect.x -= self.speed
#             if (key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH):
#                 self.rect.x += self.speed
#             if key[pygame.K_UP] and self.rect.top > 0:
#                 self.rect.y -= self.speed
#             if (key[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT):
#                 self.rect.y += self.speed

#             time_now = pygame.time.get_ticks()
#             # if key[pygame.K_SPACE] and time_now - self.last_shot > self.cooldown:
#             #     laser = Laser(self.rect.centerx, self.rect.top)
#             #     laser_group.add(laser)
#             #     self.last_shot = time_now
            
#             self.mask = pygame.mask.from_surface(self.image)

#             # self.check_collisions()

#         # for live in range(self.health_remaining - 1):
#         #    x = 5 + (live * (self.live_image.get_size()[0]))
#         #    win.blit(self.live_image, (x, 8))
        

#     def reset(self, x, y, health):
#         self.image = pygame.image.load("Sprites/jetv2.png")
#         self.img_str = pygame.image.tostring(self.image, 'RGB')
#         self.live_image = pygame.transform.rotozoom(self.image, 0, 0.7)
#         self.rect = self.image.get_rect()
#         self.rect.center = [x, y]
#         self.last_shot = pygame.time.get_ticks()
#         self.speed = 8
#         self.cooldown = 600
#         self.health_remaining = health
#         self.score = 0
#         self.laser2 = False
#         self.power_up_time = 0
#         self.alive = True
#         # self.sprites = PlayerSprite(self)
#         self.direction = None


class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False