import pygame
from pygame import Vector2

from Engine.Entity import Entity
from Engine.Drawer import drawer


class Tile(Entity):
    def __init__(self,pos,img):
        super().__init__(pos)
        self.img = img
        pass

    def draw(self):
        drawer.screen.blit(self.img, self.pos)

    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())
        return rect

    def wallCollision(self, obj):
        wallRect = self.getRect()
        wallRect.w += 4
        wallRect.h += 4
        playerRect = obj.getRect()
        if playerRect.y + playerRect.height > wallRect.y > playerRect.y:
            diff = playerRect.y + playerRect.height - wallRect.y
            obj.vel = Vector2(obj.vel.x, 0)
            obj.setPos(Vector2(obj.pos.x, playerRect.y - diff + 1))
        elif playerRect.y + playerRect.height < wallRect.y + wallRect.height and playerRect.x + playerRect.width > wallRect.x > playerRect.x:
            diff = playerRect.x + playerRect.width - wallRect.x
            obj.setPos(Vector2(playerRect.x - diff, playerRect.y))
            obj.vel = Vector2(0, obj.vel.y)
        elif playerRect.y + playerRect.height < wallRect.y + wallRect.height and playerRect.x < wallRect.x + wallRect.width and playerRect.x + playerRect.width > wallRect.x:
            diff = wallRect.x + wallRect.width - playerRect.x
            obj.setPos(Vector2(playerRect.x + diff, playerRect.y))
            obj.vel = Vector2(0, obj.vel.y)
        elif wallRect.y + wallRect.height > playerRect.y > wallRect.y:
            diff = wallRect.y + wallRect.height - playerRect.y
            obj.vel = Vector2(obj.vel.x, 0)
            obj.setPos(Vector2(obj.pos.x, playerRect.y + diff + 2))
