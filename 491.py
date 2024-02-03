#!/usr/bin/env python3

import pygame

pygame.init()

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders: Frontier')

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit
            
        pygame.display.update()


if __name__ == '__main__':
    main()