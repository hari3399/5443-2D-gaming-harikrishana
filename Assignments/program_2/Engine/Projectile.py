import math

import pygame
from pygame import Vector2

from Engine.Entity import Entity
from Engine.MSetting import mSetting
from Engine.MAssets import mAssets
from Engine.Drawer import drawer


class Projectile(Entity):
    def __init__(self, pos, force):
        self.img = mAssets.getAnimation("projectile1")
        super().__init__(pos)
        self.belongTo = ""
        self.angle = 0
        self.deathTime = 0
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

        self.applyForce(force)

    def applyForce(self, f):
        self.acc = Vector2(self.acc.x + f.x, self.acc.y + f.y)

    def update(self):
        # physic logic
        self.vel = Vector2(self.vel.x + self.acc.x, self.vel.y + self.acc.y)
        self.pos = Vector2(self.pos.x + self.vel.x, self.pos.y + self.vel.y)
        self.acc = Vector2(0, 0)

        self.applyForce(Vector2(0, mSetting.gravity))

        self.rotate()
        self.deathTime += drawer.deltaTime()
        if self.deathTime >= 100:
            self.destroy = True
        if self.pos.y >= 1000:
            self.destroy = True

        if self.pos.x < 0 or self.pos.x > 1300:
            self.destroy = True

    def rotate(self):
        # rotate projectile to it's velocity
        angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
        a = angle
        angle -= 0
        self.angle = angle

    def draw(self):
        # offset = Vector2(0, 0)
        # rotated_image, rect = drawer.rotate(self.animSheet.getCurrentFrame(), self.angle, [self.pos.x, self.pos.y],
        #                                     offset)
        # self.img = rotated_image
        # super().draw()
        self.img.draw(self.pos,self.angle)

    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.img.getWidth(), self.img.getHeight())
        return rect
