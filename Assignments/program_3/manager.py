import random

import pygame
import json
from rich import print

import pygame.display

# necessary libs for rabbitmq
from Spaceship import Spaceship


class GameManager:
    def __init__(self, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.players = {}
        self.localPlayer = None
        self.sprites = pygame.sprite.Group()

    def addPlayer(self, spriteI, bulletSpriteI, **kwargs):
        name = kwargs.get("name", None)
        player = kwargs.get("player", None)
        localPlayer = kwargs.get("localPlayer", False)

        if localPlayer:
            self.localPlayer = player.id
            self.spaceShip = player
        else:
            player = Spaceship((400, 400), spriteI, bulletSpriteI, self.create_bullet_callback, id=name)
            self.players[name] = player

    def update(self, screen):
        for id, player in self.players.items():
            player.move(screen)

        for id, player in self.players.items():
            if player.destroy:
                self.players.pop(id)
                break

    def draw(self, screen):
        try:
            for id, player in self.players.items():
                player.draw(screen)
        except:
            pass

    def callBack(self, ch, method, properties, body):
        game = method.exchange  # not used here but passed in by pika
        exchange = method.exchange  # not used here but passed in by pika
        body = json.loads(body.decode("utf-8"))  # where all the game commands are


        data = body.get("data", None)
        sender = body["sender"]
        shoot = data.get("shoot", False)
        health = data.get("health", None)
        destroy = data.get("destroy", None)
        scoreTo = data.get("scoreTo", None)
        score = data.get("score", None)
        xy = data.get("pos", None)
        velocity = data.get("vel", None)
        direction = data.get("dir", None)
        angle = data.get("angle", None)
        spriteI = data.get("spriteI", None)
        bulletSpriteI = data.get("bulletSpriteI", None)
        bulletDamage = data.get("bulletDamage", None)
        activeBulletSkill = data.get("activeBulletSkill", None)

        if self.localPlayer != sender:
            if not sender in self.players:
                self.addPlayer(spriteI, bulletSpriteI, name=sender)
                if destroy:
                    self.players[sender].destroy = destroy
                print(f"Players: {len(self.players)}")
            else:
                if xy:
                    self.players[sender].position.x = xy[0]
                    self.players[sender].position.y = xy[1]
                if velocity:
                    self.players[sender].velocity.x = velocity[0]
                    self.players[sender].velocity.y = velocity[1]
                if direction:
                    self.players[sender].direction.x = direction[0]
                    self.players[sender].direction.y = direction[1]
                if activeBulletSkill:
                    self.players[sender].activeBulletSkill = self.players[sender].activeBulletSkill
                if angle:
                    self.players[sender].angle = angle
                if shoot is True:
                    if self.players[sender].activeBulletSkill:
                        for angle in range(int(self.players[sender].angle - 5), int(self.players[sender].angle + 5), 2):
                            self.players[sender].shoot(angle, 1 + random.randrange(5, 15))
                if health:
                    self.players[sender].health = health
                if destroy:
                    self.players[sender].destroy = destroy
                if scoreTo and scoreTo in self.players:
                    self.players[scoreTo].score += 1
                if scoreTo and scoreTo == self.spaceShip.id:
                    self.spaceShip.score += 1
                    self.spaceShip.sendData()
                if score:
                    self.players[sender].score = score
                if bulletDamage:
                    self.players[sender].bulletDamage = bulletDamage
