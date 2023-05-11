import pygame
import math
from pygame.locals import *

from pygame import Vector2

class Global():

    def __init__(self):
        pygame.init()

        self.height = 720
        self.width = 1280
        self.gameOver = False
        self.currentLevel = 0
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF, 32)
        self.dt = 0
        self.clock = pygame.time.Clock()

    def calculateDeltaTime(self):
        t = self.clock.tick(60)
        self.dt = t / 1000

    def deltaTime(self):
        return self.dt

    def drawText(self, pos, text, color, size):  # draw text
        self.font = pygame.font.Font('assets/font/karma.ttf', size)
        text = self.font.render(text, True, color)
        self.screen.blit(text, (pos.x, pos.y))


mGlobal = Global()
