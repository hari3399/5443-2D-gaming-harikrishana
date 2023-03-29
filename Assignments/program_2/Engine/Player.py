import math

import pygame
from pygame import Vector2

from Engine.Entity import Entity
from Engine.MSetting import mSetting
from Engine.Projectile import Projectile
from Engine.Animation import Animation
from Engine.MAssets import mAssets
from Engine.Drawer import drawer


class Player(Entity):
    def __init__(self, pos, img, p):
        super().__init__(pos)
        self.img = img
        self.speed = 3
        if p == 1:
            self.gunImg = mAssets.getImg("gun")
        else:
            self.gunImg = mAssets.getImg("gun2")
        self.angle = 0
        self.shotY = 7
        self.p = p

        self.holding = False

        self.projectilePos = Vector2(0, 0)

        self.shootDir = Vector2(0, 0)
        self.projectileSpeed = 1
        self.isMissie = False

        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def applyForce(self, f):
        self.acc = Vector2(self.acc.x + f.x, self.acc.y + f.y)

    def update(self):
        # physic
        self.vel = Vector2(self.vel.x + self.acc.x, self.vel.y + self.acc.y)
        self.pos = Vector2(self.pos.x + self.vel.x, self.pos.y + self.vel.y)
        self.acc = Vector2(0, 0)

        self.applyForce(Vector2(0, mSetting.gravity)) # gravity

        # screen check
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > 1280 - 32:
            self.pos.x = 1280 - 32

        if self.p != mSetting.currentTurn:
            return
        self.rotateGun()

    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())
        return rect

    def setPos(self, pos):
        self.pos = pos

    def draw(self):
        # draw player
        drawer.screen.blit(self.img, self.pos)

        # draw gun
        if self.p == 1:
            gunPos = Vector2(self.pos.x + 34, self.pos.y + 48)
        else:
            gunPos = Vector2(self.pos.x + 27, self.pos.y + 43)
        offset = Vector2(0, 0)
        rotated_image, rect = Animation.rotate(self.gunImg, self.angle, [gunPos.x, gunPos.y], offset)
        drawer.screen.blit(rotated_image, rect)

        # use for projectile position
        self.projectilePos = gunPos + self.shootDir * 20
        self.projectilePos.x -= 42
        self.projectilePos.y -= 42

        # draw power when holding
        if self.holding:
            self.projectileSpeed += 0.3
            if self.projectileSpeed >= 30:
                self.projectileSpeed = 30

        if self.holding:
            drawer.drawText(Vector2(self.pos.x + 5, self.pos.y - 15), "{:.2f}".format(self.projectileSpeed),
                            (200, 200, 1), 20)

    def rotateGun(self):
        # rotate gun with mouse
        mouseX, mouseY = pygame.mouse.get_pos()
        cannonX = self.pos.x + 34
        cannonY = self.pos.y + 48

        dirX = mouseX - cannonX
        dirY = mouseY - cannonY
        angle = math.degrees(math.atan2(dirY, dirX))
        a = angle
        angle += 90
        self.angle = angle
        self.shootDir = Vector2(math.cos(math.radians(a)), math.sin(math.radians(a))).normalize()

    def onMouseDown(self, event):
        if self.p != mSetting.currentTurn:
            return
        self.vel = Vector2(0, 0)
        self.holding = True
        self.projectileSpeed = 5
        pass

    def onMouseUp(self, event):
        if self.p != mSetting.currentTurn:
            return
        self.shotY = 7
        self.holding = False
        self.particleScale = 10
        self.vel = Vector2(0, 0)

    def getProjectile(self):
        # create projectile with force (direction to the mouse)
        force = self.shootDir * self.projectileSpeed
        projectile = Projectile(self.projectilePos, force)
        return projectile

    def onKeyUp(self, keycode):
        if keycode == pygame.K_a:
            if self.vel.x == -self.speed:
                self.vel.x = 0
        elif keycode == pygame.K_d:
            if self.vel.x == self.speed:
                self.vel.x = 0

    def onKeyDown(self, keycode):
        if keycode == pygame.K_a:
            self.vel.x = -self.speed
        elif keycode == pygame.K_d:
            self.vel.x = self.speed
