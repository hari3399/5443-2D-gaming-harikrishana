import math

import pygame

from GameObject import GameObject
from Global import mGlobal
from utils import load_sprite


class Bullet(GameObject):
    def __init__(self, position, velocity, id, spriteIndex, damage):
        super().__init__(position, load_sprite("bullet" + str(spriteIndex)), velocity)
        self.id = id
        self.damage = 10
        self.sizeX = self.sprite.get_width()
        self.sizeY = self.sprite.get_height()
        self.angle = 0
        self.position.x += self.sizeX / 2
        self.position.y += self.sizeY/2

    def move(self, surface):
        self.position = self.position + self.velocity

        angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x))
        angle += 90
        self.angle = angle

    def rotate(self,surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect

    def draw(self, surface):

        # update scale
        self.sizeX -= mGlobal.deltaTime() * 12
        self.sizeY -= mGlobal.deltaTime() * 12
        self.damage -= mGlobal.deltaTime() * 6

        if self.sizeX < 1:
            self.sizeX = 1
        if self.sizeY < 1:
            self.sizeY = 1
        if self.damage < 1:
            self.damage = 1

        sprite = pygame.transform.scale(self.sprite,(int(self.sizeX),int(self.sizeY)))
        blit_position = pygame.Vector2(self.position.x - self.sizeX/2, self.position.y - self.sizeY/2)
        self.radius = self.sizeX/2

        offset = pygame.Vector2(0, 0)
        rotated_image, rect = self.rotate(sprite, self.angle, [blit_position.x,blit_position.y], offset)
        surface.blit(rotated_image, rect)