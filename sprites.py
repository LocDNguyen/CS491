import pygame
from constants import *
import numpy as np
from animation import Animator

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("Sprites/spritesheet_jetv2.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        self.sheet2 = pygame.image.load("Sprites/explosion.png").convert()
        transcolor = self.sheet2.get_at((0,0))
        self.sheet2.set_colorkey(transcolor)
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

class PlayerSprite(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.character = character
        self.character.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (0, 0)

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((185, 0), (185, 0)))#(55, 0), (120, 0), (185, 0), (250, 0)))
        self.animations[RIGHT] = Animator(((120, 65), (120, 65)))#(0, 65), (60, 65), (120, 65), (185, 65)))
        self.animations[UP] = Animator(((0, 0), (0, 0), (0, 0), (0, 0)))
        self.animations[DOWN] = Animator(((0, 0), (0, 0), (0, 0), (0, 0)))
        self.animations[DEATH] = Animator(((0, 0), (0, 0)), speed=6, loop=False)

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
            elif self.character.direction == STOP:
                self.character.image = self.getImage(*self.stopimage)
        else:
            self.character.image = self.getImage2(*self.animations[DEATH].update(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 4*TILEWIDTH, 4*TILEHEIGHT)

    def getImage2(self, x, y):
        return Spritesheet.getImage2(self, x, y, 6*TILEWIDTH, 6*TILEHEIGHT)

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