# Sabin Dheke and Hari Krishna
# CMPS 5443 
# Advance topic: 2D Games
# Assignment 2

import pygame
from pygame import Vector2

from Engine.Explosion1 import Explosion1
from Engine.Explosion2 import Explosion2
from Engine.MSetting import mSetting
from Engine.Player import Player
from Engine.Projectile import Projectile
from Engine.Tile import Tile
from Engine.Level1 import  Level1
from Engine.Drawer import drawer
from Engine.MAssets import mAssets


class MyGame:
    def __init__(self):
        self.map = None

        self.gameObjects = []
        self.currentProjectile = None

        self.winner = None
        self.player1 = None
        self.player2 = None

        self.newGame()

    # new game
    def newGame(self):
        self.winner = None
        self.gameObjects = Level1().gameObjects

        # create players
        self.player1 = Player(Vector2(300,300),mAssets.getImg("player1"),1)
        self.player2 = Player(Vector2(900, 200), mAssets.getImg("player2"),2)

        # self.player2 = Tank(Vector2(1070, 100))
        self.gameObjects.append(self.player1)
        self.gameObjects.append(self.player2)

    def update(self):

        # check collisio for player
        self.playerCollisionCheck(self.player1)
        self.playerCollisionCheck(self.player2)

        # update all game objects
        for object in self.gameObjects:
            object.update()

            # check current projectile
            if isinstance(object,Projectile):
                self.projectileCollideWall(object) # check projectile with wall
                if object.destroy: # destroy projectile logic
                    self.gameObjects.remove(object)
                    self.currentProjectile = None
                    # self.gameObjects.append(Explosion(Vector2(object.pos.x - 32,object.pos.y - 32)))
                    if mSetting.currentTurn == 1:
                        mSetting.currentTurn = 2
                    else:
                        mSetting.currentTurn = 1
                    break
            if object.destroy:
                self.gameObjects.remove(object)


        # game over if player position y > 1000
        if self.player1.pos.y > 1000 or self.player1.pos.x < 10: # or self.player1.pos.x > 1900:
            self.winner = 1
            return
        if self.player2.pos.y > 1000 or self.player2.pos.x > 1200: # or self.player2.pos.x < 10:
            self.winner = 2
            return

           

    def playerCollisionCheck(self, player):
        for obj in self.gameObjects:
            if isinstance(obj, Tile): # player wall collision
                if drawer.collide(player, obj):
                    obj.wallCollision(player)
            # projectile and player1 collision logic
            if isinstance(obj, Projectile) and drawer.collide(player, obj) and player.p == 1 and obj.belongTo != player.p:
                self.winner = 2
                player.destroy = True
                self.gameObjects.append(Explosion2(Vector2(player.pos.x + 24,player.pos.y + 24)))
            # projectile and player2 collision logic
            if isinstance(obj, Projectile) and drawer.collide(player, obj) and player.p == 2 and obj.belongTo != player.p:
                self.winner = 1
                player.destroy = True
                self.gameObjects.append(Explosion2(Vector2(player.pos.x + 24,player.pos.y + 24)))

    def projectileCollideWall(self, projectile):
        for obj in self.gameObjects:
            if isinstance(obj,Tile):
                if drawer.collide(projectile, obj): # current projectile collide with wall
                    obj.destroy = True
                    projectile.destroy = True

        # set destroy Flag to any wall in radius of 100
        if projectile.destroy:
            for obj in self.gameObjects:
                if isinstance(obj,Tile) and drawer.distance(projectile.pos.x, projectile.pos.y, obj.pos.x, obj.pos.y) < 100:
                    obj.destroy = True

    def onKeyDown(self, key):

        if self.winner is not None:
            if key == pygame.K_SPACE:
                self.newGame()

            # key left right to change gravity setting
            if key == pygame.K_LEFT:
                mSetting.gravity -= 0.1
                if mSetting.gravity < 0.1:
                    mSetting.gravity = 0.1
            elif key == pygame.K_RIGHT:
                mSetting.gravity += 0.1
                if mSetting.gravity > 1:
                    mSetting.gravity = 1
            return


        if self.currentProjectile is not None:
            return

        if mSetting.currentTurn == 1:
            self.player1.onKeyDown(key)
        else:
            self.player2.onKeyDown(key)




    def onKeyUp(self, key):
        if self.winner is not None:
            return
        if self.currentProjectile != None:
            return

        if mSetting.currentTurn == 1:
            self.player1.onKeyUp(key)
        else:
            self.player2.onKeyUp(key)

    def onMouseDown(self, event):
        if self.winner is not None:
            return
        if self.currentProjectile != None:
            return

        if mSetting.currentTurn == 1:
            self.player1.onMouseDown(event)
        else:
            self.player2.onMouseDown(event)

    def onMouseUp(self, event):
        if self.winner is not None:
            return

        # add projectile to gameObjects list after mouse button up event

        if mSetting.currentTurn == 1:
            self.player1.onMouseUp(event)
            projectile = self.player1.getProjectile()
            projectile.belongTo = 1
            self.gameObjects.append(projectile)
            self.currentProjectile = projectile
            self.gameObjects.append(Explosion1(Vector2(projectile.pos.x-12,projectile.pos.y-12))) # explosion when shoot

        else:
            self.player2.onMouseUp(event)
            projectile = self.player2.getProjectile()
            projectile.belongTo = 2
            self.gameObjects.append(projectile)
            self.currentProjectile = projectile
            self.gameObjects.append(Explosion1(Vector2(projectile.pos.x-12,projectile.pos.y-12))) # explosion when shoot

    def draw(self):
        for obj in self.gameObjects:
            obj.draw()

        if self.winner == 1:
            drawer.drawText(Vector2(430, 200), "Game Over!! Player #2 wins", (244, 244, 23), 43)
        elif self.winner == 2:
            drawer.drawText(Vector2(430, 200), "Game Over!! Player #1 wins", (244, 244, 23), 43)

        if self.winner is not None:
            drawer.drawText(Vector2(480, 340), "Press any key to restart!", (166, 23, 23), 32)
            drawer.drawText(Vector2(550, 300), "gravity : " + " < {:.2f} >".format(mSetting.gravity * 100), (23, 23, 244), 24)

