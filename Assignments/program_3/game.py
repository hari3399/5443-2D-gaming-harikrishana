import random
import sys

import pygame
from rich import json

from Global import mGlobal
from Spaceship import Spaceship
from manager import GameManager
from utils import load_sprite, print_text, mykwargs
from urllib.request import urlopen


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self, queue, playerId, creds):

        self._init_pygame()
        mGlobal.calculateDeltaTime()
        self.asteroids = []
        self.bullets = []

        # globals = Globals(x, y)
        self.manager = GameManager(self.bullets.append)
        localSpaceShip = Spaceship((400, 400), None, None, self.bullets.append,
                                   id=playerId, creds=creds, callback=self.manager.callBack
                                   )
        self.manager.addPlayer(None, None, player=localSpaceShip, localPlayer=True)
        # set the window title
        pygame.display.set_caption(f"{creds['user']}")

        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.gameStatus = "playing"
        self.spaceship = localSpaceShip

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Outlaw Star")

    def _handle_input(self):
        if self.gameStatus == "lose":
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                    self.spaceship
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
            ):
                self.spaceship.sendData(None, True)
                self.spaceship.shoot(self.spaceship.angle, 10)
                if self.spaceship.activeBulletSkill:
                    for angle in range(int(self.spaceship.angle - 5), int(self.spaceship.angle + 5), 2):
                        self.spaceship.shoot(angle, 1 + random.randrange(5, 15))

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
                self.spaceship.sendData()
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
                self.spaceship.sendData()
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate(1)
                self.spaceship.sendData()
            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship.accelerate(-1)
                self.spaceship.sendData()
            if is_key_pressed[pygame.K_s]:
                self.spaceship.stopShip()
            if is_key_pressed[pygame.K_9]:
                self.spaceship.score += 50

    def _process_game_logic(self):
        if self.gameStatus == "lose":
            return

        for id, player in self.manager.players.items():
            for bullet in self.bullets[:]:
                if bullet.collides_with(player) and bullet.id != id:
                    self.bullets.remove(bullet)
                    break

        self.manager.update(mGlobal.screen)
        for game_object in self._get_game_objects():
            game_object.move(mGlobal.screen)

        for bullet in self.bullets[:]:
            if bullet.collides_with(self.spaceship) and bullet.id != self.spaceship.id:
                self.spaceship.gotHit(int(bullet.damage))
                self.spaceship.sendData(scoreTo=bullet.id)
                self.bullets.remove(bullet)
                break

        for bullet in self.bullets[:]:
            if not mGlobal.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if self.spaceship.destroy:
            self.spaceship.sendData()
            self.message = "You lose!"
            self.gameStatus = "lose"
        mGlobal.calculateDeltaTime()


    def _draw(self):
        # transparent background
        my_surface = pygame.Surface((1280, 720))
        my_surface = my_surface.convert_alpha()
        my_surface.fill((23, 23, 23, 100))
        mGlobal.screen.blit(my_surface, (0, 0))

        self.manager.draw(mGlobal.screen)

        for game_object in self._get_game_objects():
            game_object.draw(mGlobal.screen)

        if self.message:
            print_text(mGlobal.screen, self.message, self.font)

        self.drawScoreTable()

        pygame.display.flip()
        self.clock.tick(60)

    def drawScoreTable(self):
        # info
        mGlobal.drawText(pygame.Vector2(950, 20), "Collect 50 scores to upgrade bullets!", (23, 233, 233), 16)
        mGlobal.drawText(pygame.Vector2(1000, 50), "Press '9' to hack score!", (233, 233, 233), 16)
        mGlobal.drawText(pygame.Vector2(1100, 630), "S : stop (" + str(self.spaceship.thrustStop) + ")", (23, 233, 233),
                         16)
        mGlobal.drawText(pygame.Vector2(1100, 660), "UP/DOWN : thrust", (255, 23, 233), 16)
        mGlobal.drawText(pygame.Vector2(1100, 690), "LEFT/RIGHT : rotate", (255, 23, 23), 16)


        # player score and health bar
        mGlobal.drawText(pygame.Vector2(3 * 110, 10), self.spaceship.id + ": " + str(self.spaceship.score),
                         (255, 233, 34), 16)
        pygame.draw.rect(mGlobal.screen, (233, 233, 233), pygame.Rect(20, 20, 3 * 100, 5), 2)
        for i in range(0, self.spaceship.health + 1):
            pygame.draw.rect(mGlobal.screen, (23, 233, 23), pygame.Rect(20, 20, 3 * i, 5))

        y = 40
        for id, player in self.manager.players.items():
            if id == self.spaceship.id:
                continue
            mGlobal.drawText(pygame.Vector2(3 * 110, y - 10), player.id + ": " + str(player.score), (233, 233, 233), 16)
            pygame.draw.rect(mGlobal.screen, (233, 233, 233), pygame.Rect(20, y, 3 * 100, 5), 2)
            for i in range(0, player.health + 1):
                pygame.draw.rect(mGlobal.screen, (233, 23, 23), pygame.Rect(20, y, 3 * i, 5))
            y += 30

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
