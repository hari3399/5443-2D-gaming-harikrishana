import math

import pygame
from pygame import Vector2

from Engine.Entity import Entity
from Engine.MSetting import mSetting
from Engine.MAssets import mAssets
from Engine.Drawer import drawer


class Explosion2(Entity):
    def __init__(self, pos):
        self.anim = mAssets.getAnimation("explosion2")
        self.anim.reset()
        super().__init__(pos)
        self.deathTime = 0

    def update(self):
        self.deathTime += drawer.deltaTime()
        if self.deathTime >= 1:
            self.destroy = True

    def draw(self):
        self.anim.draw(self.pos, 0)
