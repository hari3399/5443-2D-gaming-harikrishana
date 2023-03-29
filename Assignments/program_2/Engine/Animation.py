import pygame
from pygame import Vector2

from Engine.Drawer import drawer


class Animation:

    def __init__(self, texture, rows, cols, ffrom, fto, delay, loop):

        self.texture = texture
        self.rows = rows
        self.cols = cols

        self.sheet = texture
        self.frames = []

        self.width = self.sheet.get_rect().width
        self.height = self.sheet.get_rect().height

        # cut images by row and column and save them to a list

        sizeRow = self.sheet.get_rect().height / rows
        sizeCol = self.sheet.get_rect().width / cols
        for row in range(0, rows):
            for col in range(0, cols):
                img = self.getImgWithRect((col * sizeCol, row * sizeRow, sizeCol, sizeRow), (0, 0, 0))
                self.frames.append(img)
        print(self.frames)
        self.countTime = 0
        self.ffrom = ffrom
        self.fto = fto
        self.current = 0
        self.time = delay
        self.loop = loop

    def reset(self):
        self.current = 0
        self.countTime = 0

    def playAnimation(self):
        # play animation from frameIndex to frameIndex
        self.countTime += drawer.deltaTime()
        if self.countTime >= self.time:
            self.countTime = 0
            self.current += 1
            if self.current > self.fto and self.loop:
                self.current = self.ffrom
            elif self.current > self.fto and not self.loop:
                self.current = self.fto

    def stopAnimation(self):
        pass

    def getImgWithRect(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    @staticmethod
    def rotate(surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect

    def draw(self, pos,angle):
        self.playAnimation()

        #img = self.frames[self.current]
        #offset = Vector2(0, 0)
        #rotated_image, rect = self.rotate(img, angle, [pos.x, pos.y], offset)
        #drawer.screen.blit(rotated_image, rect)
        drawer.screen.blit(self.frames[self.current],pos)

    def getWidth(self):
        return self.frames[self.current].get_width()

    def getHeight(self):
        return self.frames[self.current].get_height()