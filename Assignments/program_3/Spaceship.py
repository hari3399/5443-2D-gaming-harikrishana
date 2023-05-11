import math
import random

import pygame
from pygame import Vector2
from pygame.transform import rotozoom

from Bullet import Bullet
from GameObject import GameObject
from Global import mGlobal
from messenger import Messenger
from utils import load_sound, load_sprite

UP = Vector2(0, -1)


class Spaceship(GameObject):
    MANEUVERABILITY = 6
    ACCELERATION = 0.10
    BULLET_SPEED = 10

    def __init__(self, position, spriteIndex, bulletSpriteI, create_bullet_callback, **kwargs):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        self.creds = kwargs.get("creds", None)
        self.callback = kwargs.get("callback", None)
        self.id = kwargs.get("id", None)
        if self.creds is not None:
            self.messenger = Messenger(self.creds, self.callback)
        self.lastBroadcast = pygame.time.get_ticks()
        self.broadCastDelay = 0
        if spriteIndex is None:
            self.spriteI = random.randrange(0, 10)
            self.bulletSpriteIndex = random.randrange(0, 7)
        else:
            self.spriteI = spriteIndex
            self.bulletSpriteIndex = bulletSpriteI
        self.aimSprite = load_sprite("aim")
        super().__init__(position, load_sprite("space_ship" + str(self.spriteI)), Vector2(0))
        self.healthGeneTime = 60
        self.health = 100
        self.score = 0
        self.thrustStop = 2
        self.activeBulletSkill = False
        self.bulletDamage = 10
        self.angle = 0

    def timeToBroadCast(self):
        """check to see if there was enough delay to broadcast again"""
        return pygame.time.get_ticks() - self.lastBroadcast > self.broadCastDelay

    def broadcastData(self, data):
        if self.timeToBroadCast():
            self.messenger.send(
                target="broadcast", sender=self.id, player=self.id, data=data
            )
            self.lastBroadcast = pygame.time.get_ticks()
            return True

        return False

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self, dir):
        self.velocity += self.direction * self.ACCELERATION * dir

    def stopShip(self):
        if self.velocity.x != 0 and self.velocity.y != 0 and self.thrustStop > 0:
            self.thrustStop -= 1
            self.velocity = Vector2(0, 0)

    def draw(self, surface):
        ###
        self.healthGeneTime -= mGlobal.deltaTime()
        if self.healthGeneTime < 0:
            self.healthGeneTime = 60
            self.health += 10
            if self.health > 100:
                self.health = 100
            self.sendData()

        if self.score >= 20:
            self.activeBulletSkill = True
            self.bulletDamage = 20

        self.angle = math.atan2(self.direction.y, self.direction.x) * 180 / math.pi
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

        y = math.sin(math.radians(angle))
        dir = Vector2(self.direction.x, self.direction.y)
        aimPos = self.position + dir * 100
        surface.blit(self.aimSprite, aimPos)

    def sendData(self, scoreTo=None, shoot=False):
        self.broadcastData(
            {
                "pos": (self.position.x, self.position.y),
                "vel": (self.velocity.x, self.velocity.y),
                "dir": (self.direction.x, self.direction.y),
                "shoot": shoot,
                "score": self.score,
                "spriteI": self.spriteI,
                "bulletSpriteI": self.bulletSpriteIndex,
                "bulletDamage": self.bulletDamage,
                "activeBulletSkill": self.activeBulletSkill,
                "angle": self.angle,
                "health": self.health,
                "destroy": self.destroy,
                "scoreTo": scoreTo,
            }
        )

    def shoot(self, angle, speed):
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))
        bullet_velocity = Vector2(x, y) * speed + self.velocity
        bullet = Bullet(self.position, bullet_velocity, self.id, self.bulletSpriteIndex, self.bulletDamage)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def gotHit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroy = True
