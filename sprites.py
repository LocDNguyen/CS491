import pygame
from constants import *
import numpy as np
from animation import Animator

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("Sprites/spritesheet_jetv4.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        self.sheet2 = pygame.image.load("Sprites/explosion2.png").convert()
        transcolor = self.sheet2.get_at((0,0))
        self.sheet2.set_colorkey(transcolor)
        self.sheet3 = pygame.image.load("Sprites/spritesheet_blue_alien.png").convert()
        transcolor = self.sheet3.get_at((0,0))
        self.sheet3.set_colorkey(transcolor)
        self.sheet4 = pygame.image.load("Sprites/pink_alien.png").convert()
        transcolor = self.sheet4.get_at((0,0))
        self.sheet4.set_colorkey(transcolor)
        #width = int(self.sheet.get_width() / BASETILEWIDTH * 9)
        #height = int(self.sheet.get_height() / BASETILEHEIGHT * 8)
        #self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        #x *= TILEWIDTH
        #y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())
    
    def getImage2(self, x, y, width, height):
        #x *= TILEWIDTH
        #y *= TILEHEIGHT
        self.sheet2.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet2.subsurface(self.sheet2.get_clip())
    
    def getImage3(self, x, y, width, height):
        #x *= TILEWIDTH
        #y *= TILEHEIGHT
        self.sheet3.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet3.subsurface(self.sheet3.get_clip())
    
    def getImage4(self, x, y, width, height):
        #x *= TILEWIDTH
        #y *= TILEHEIGHT
        self.sheet4.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet4.subsurface(self.sheet4.get_clip())

class PlayerSprite(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.character = character
        self.character.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (0, 0)

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((130, 64), (195, 64), (260, 64), (325, 64), (390, 64), (455, 64), (520, 64), (585, 64)), loop=False)
        self.animations[RIGHT] = Animator(((60, 0), (125, 0), (190, 0), (255, 0), (320, 0), (385, 0), (450, 0), (515, 0), (580, 0)), loop=False)
        self.animations[UP] = Animator(((0, 0), (0, 0), (0, 0), (0, 0)))
        self.animations[DOWN] = Animator(((0, 0), (0, 0), (0, 0), (0, 0)))
        self.animations[DEATH] = Animator(((20, 20), (150, 20), (280, 20), (410, 20), (540, 20), (20, 150), (150, 150), (280, 150), (410, 150), (540, 150), (20, 280), (150, 280), (280, 280), (410, 280), (540, 280), (20, 410), (150, 410), (280, 410), (410, 410), (540, 410), (20, 540), (150, 540), (280, 540), (410, 540), (540, 540)), speed=6, loop=False)
        self.animations[HIT] = Animator(((0, 65), (0, 65)))

    def update(self, dt):
        if self.character.alive == True:
            if self.character.direction == LEFT:
                self.character.image = self.getImage(*self.animations[LEFT].update(dt))
                self.stopimage = (0, 0)
            elif self.character.direction == RIGHT:
                self.character.image = self.getImage(*self.animations[RIGHT].update(dt))
                self.stopimage = (0, 0)
            elif self.character.direction == DOWN:
                self.character.image = self.getImage(*self.animations[DOWN].update(dt))
                self.stopimage = (0, 0)
            elif self.character.direction == UP:
                self.character.image = self.getImage(*self.animations[UP].update(dt))
                self.stopimage = (0, 0)
            elif self.character.direction == HIT:
                self.character.image = self.getImage(*self.animations[HIT].update(dt))
                self.stopimage = (0, 0)
            elif self.character.direction == STOP:
                self.character.image = self.getImage(*self.stopimage)
                self.reset()
        else:
            self.character.image = self.getImage2(*self.animations[DEATH].update(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 64, 64)

    def getImage2(self, x, y):
        return Spritesheet.getImage2(self, x, y, 100, 114)
    
class AlienSprites(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.x = {ABLUE:0, APINK:2, AGREEN:4, APURPLE:6}
        self.character = character
        self.character.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()

    def defineAnimations(self):
        self.animations[MOVE] = Animator(((0, 64), (64, 64)), speed=1)
        self.animations[EXPLODE] = Animator(((0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0), (384, 0), (448, 0), (512, 0), (576, 0)), loop = False)
        self.animations[HIT] = Animator(((128, 64), (128, 64)))

    def update(self, dt):
        if self.character.alive:
            if self.character.type == 'blue':
                self.character.image = self.getImage(*self.animations[MOVE].update(dt))
                if self.character.hit == True:
                    self.character.image = self.getImage(*self.animations[HIT].update(dt))
                    self.character.hit = False
            if self.character.type == 'pink':
                self.character.image = self.getImage2(*self.animations[MOVE].update(dt))
                if self.character.hit == True:
                    self.character.image = self.getImage2(*self.animations[HIT].update(dt))
                    self.character.hit = False
        else:
            if self.character.type == 'blue':
                self.character.image = self.getImage(*self.animations[EXPLODE].update(dt))
            if self.character.type == 'pink':
                self.character.image = self.getImage2(*self.animations[EXPLODE].update(dt))

    def getStartImage(self):
        if self.character.type == 'blue':
            return self.getImage(0, 0)
        if self.character.type == 'pink':
            return self.getImage2(0, 0)
        # if self.character.name == 6:
        #     return self.getImage(7.4, 12)
        # if self.character.name == 7:
        #     return self.getImage(7.4, 14)

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()
        self.character.image = self.getStartImage()

    def getImage(self, x, y):
        return Spritesheet.getImage3(self, x, y, 64, 64)
    
    def getImage2(self, x, y):
        return Spritesheet.getImage4(self, x, y, 64, 64)
    
# class AlienLasers(Spritesheet):
#     def __init__(self, character):
#         Spritesheet.__init__(self)
#         self.x = {ABLUE:0, APINK:2, AGREEN:4, APURPLE:6}
#         self.character = character
#         self.character.image = self.getStartImage()
#         self.animations = {}
#         self.defineAnimations()

#     def defineAnimations(self):
#         self.animations[SHOOT] = Animator(((0, 0), (0, 0)), speed=1)

#     def update(self, dt):
#         if self.character.type == 'blue':
#             self.character.image = self.getImage(*self.animations[SHOOT].update(dt))
        # if self.character.name == 7:
        #     if self.character.direction == LEFT:
        #         self.character.image = self.getImage(*self.animations[CLEFT].update(dt))
        #     elif self.character.direction == RIGHT:
        #         self.character.image = self.getImage(*self.animations[CRIGHT].update(dt))
        #     elif self.character.direction == DOWN:
        #         self.character.image = self.getImage(*self.animations[CDOWN].update(dt))
        #     elif self.character.direction == UP:
        #         self.character.image = self.getImage(*self.animations[CUP].update(dt))
        # elif self.character.mode.current == FRIGHT:
        #     self.character.image = self.getImage(*self.animations[FRIGHT].update(dt))
        # elif self.character.mode.current == SPAWN:
        #     if self.character.direction == LEFT:
        #         self.character.image = self.getImage2(8, 8)
        #     elif self.character.direction == RIGHT:
        #         self.character.image = self.getImage2(8, 10)
        #     elif self.character.direction == DOWN:
        #         self.character.image = self.getImage2(8, 6)
        #     elif self.character.direction == UP:
        #        self.character.image = self.getImage2(8, 4)

    # def getStartImage(self):
    #     if self.character.type == 'blue':
    #         return self.getImage(0, 0)
    #     # if self.character.name == 5:
    #     #     return self.getImage(10.95, 10)
    #     # if self.character.name == 6:
    #     #     return self.getImage(7.4, 12)
    #     # if self.character.name == 7:
    #     #     return self.getImage(7.4, 14)

    # def reset(self):
    #     for key in list(self.animations.keys()):
    #         self.animations[key].reset()
    #     self.character.image = self.getStartImage()

    # def getImage(self, x, y):
    #     return Spritesheet.getImage3(self, x, y, 64, 64)

# class LifeSprites(Spritesheet):
#     def __init__(self, numlives):
#         Spritesheet.__init__(self)
#         self.resetLives(numlives)

#     def removeImage(self):
#         if len(self.images) > 0:
#             self.images.pop(0)

#     def addImage(self):
#         self.images.append(self.getImage(0,0))

#     def resetLives(self, numlives):
#         self.images = []
#         for i in range(numlives):
#             self.images.append(self.getImage(0,0))

#     def getImage(self, x, y):
#         return Spritesheet.getImage2(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

# class MazeSprites(Spritesheet):
#     def __init__(self, mazefile, rotfile):
#         Spritesheet.__init__(self)
#         self.data = self.readMazeFile(mazefile)
#         self.rotdata = self.readMazeFile(rotfile)

#     def getImage(self, x, y):
#         return Spritesheet.getImage2(self, x, y, TILEWIDTH, TILEHEIGHT)

#     def readMazeFile(self, mazefile):
#         return np.loadtxt(mazefile, dtype='<U1')

#     def constructBackground(self, background, y):
#         for row in list(range(self.data.shape[0])):
#             for col in list(range(self.data.shape[1])):
#                 if self.data[row][col].isdigit():
#                     x = int(self.data[row][col]) + 12
#                     sprite = self.getImage(x, y)
#                     rotval = int(self.rotdata[row][col])
#                     sprite = self.rotate(sprite, rotval)
#                     background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
#                 elif self.data[row][col] == '=':
#                     sprite = self.getImage(10, 8)
#                     background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

#         return background

#     def rotate(self, sprite, value):
#         return pygame.transform.rotate(sprite, value*90)