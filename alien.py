# Base code from Michael Breslavsky https://github.com/breslavmich/jet_fighter_multiplayer/tree/master

import math
import random
import pygame
from math import sin, cos, radians
from bullet import Bullet


def rot_center(image):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    return orig_rect


class Alien:
    def __init__(self, screen_width: int, screen_height: int, plane_image: pygame.Surface, x: int, y: int):
        self.x = x
        self.y = y
        self.image = plane_image

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.speed = 3
        self.move_direction = 1

        self.bullets = []

    def keep_in_map(self) -> None:
        """Keeping the jet in the bounds of the screen"""
        width, height = self.image.get_size()
        rect = rot_center(self.image)
        if self.x <= 0 or (self.x + width) >= self.screen_width:
            self.move_direction *= -1
            self.y += 8

    def draw(self, screen: pygame.Surface) -> None:
        """Drawing the jet on the screen"""
        image = rot_center(self.image)
        image.x = self.x
        image.y = self.y
        screen.blit(self.image, (self.x, self.y))
        self.draw_bullets(screen)

    def update(self, enemy_bullets: list, hits_list: list) -> None:
        """Updating the jet's parameters"""
        # Updating the position
        self.keep_in_map()
        self.x += self.move_direction

        # Updating all bullets
        for bullet in self.bullets:
            if bullet.time_alive > 200:
                self.bullets.remove(bullet)
            else:
                bullet.update()
        # Checking if plane was hit
        self.check_hits(enemy_bullets, hits_list)

    # def change_direction(self):
    #     for alien in alien_group:
    #         alien.rect.y += 8
    #         alien.move_direction *= -1

    # def check_edges(self):
    #     screen_rect = screen.get_rect()
    #     return self.rect.right >= screen_rect.right or self.rect.left <= 0

    # def edge_check():
    #     for alien in alien_group:
    #         if alien.check_edges():
    #             alien.change_direction()
    #             break

    def check_hits(self, enemy_bullets: list, hits_list: list):
        """Checking if plane was hit"""
        for bullet in enemy_bullets:
            if math.dist((self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2),
                         (bullet.x, bullet.y)) < 13 + bullet.radius:
                # Checking if bullet hit the plane
                hits_list.append(bullet)
                enemy_bullets.remove(bullet)

    def shoot(self) -> None:
        """Shooting a bullet"""
        bullet = Bullet(self.screen_width, self.screen_height, int(self.x),
                        int(self.y), self.angle, self.is_white)  # Creating a bullet
        self.bullets.append(bullet)  # Adding bullet to the list

    def draw_bullets(self, screen: pygame.Surface) -> None:
        """Drawing all the bullets for the plane"""
        for bullet in self.bullets:
            bullet.draw(screen)

    def to_dict(self) -> dict:
        """Returning a description dictionary of the parameters of the plane to send to the client"""
        description = vars(self).copy()
        desc_bullets = []
        try:
            del description['image']
            del description['screen_width']
            del description['screen_height']
        except:
            pass
        for bullet in description['bullets']:
            desc_bullets.append(bullet.to_dict())
        description['bullets'] = desc_bullets
        return description

    def new_bullet_from_dict(self, description_dict: dict) -> None:
        """Creating a new bullet based on parameters from a dictionary"""
        new_bullet = Bullet(screen_width=description_dict['screen_width'],
                            screen_height=description_dict['screen_height'],
                            x=description_dict['x'],
                            y=description_dict['y'],
                            angle=description_dict['angle'],
                            is_white=description_dict['is_white'])
        self.bullets.append(new_bullet)

    def data_from_dict(self, description_dict: dict) -> None:
        """Updating a jet's parameters based on parameters from a dictionary"""
        self.x = description_dict['x']
        self.y = description_dict['y']

        self.speed = description_dict['speed']

        self.bullets = []
        for i in range(len(description_dict['bullets'])):
            self.new_bullet_from_dict(description_dict['bullets'][i])
