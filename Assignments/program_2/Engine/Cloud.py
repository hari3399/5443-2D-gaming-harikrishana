import random

from Engine.Entity import Entity
from Engine.Drawer import drawer


class Cloud(Entity):
    def __init__(self, pos, img):
        super().__init__(pos)
        self.img = img
        self.speed = random.randrange(2,5)

    def update(self):
        self.pos.x -= self.speed
        if self.pos.x < 0:
            self.pos.x = 1300

    def draw(self):
        drawer.screen.blit(self.img, self.pos)