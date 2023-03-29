import pygame

from Engine.Animation import Animation


class MAssets:
    def __init__(self):
        self.images = {
            'tree': pygame.image.load("images/tree.png").convert_alpha(),
            'cloud': pygame.image.load("images/cloud.png").convert_alpha(),
            'sun': pygame.image.load("images/sun.png").convert_alpha(),
            'player1': pygame.image.load("images/player1.png").convert_alpha(),
            'player2': pygame.image.load("images/player2.png").convert_alpha(),
            'gun': pygame.image.load("images/gun.png").convert_alpha(),
            'gun2': pygame.image.load("images/gun2.png").convert_alpha(),
            'grass1': pygame.image.load("images/grass1.png").convert_alpha(),
            'grass2': pygame.image.load("images/grass2.png").convert_alpha(),
            'grass3': pygame.image.load("images/grass3.png").convert_alpha(),
            'projectileSheet': pygame.image.load("images/projectileSheet.png").convert_alpha(),
            'projectileSheet2': pygame.image.load("images/projectileSheet2.png").convert_alpha(),
            'explosionSheet1': pygame.image.load("images/explosion1.png").convert_alpha(),
            'explosionSheet2': pygame.image.load("images/explosion-6.png").convert_alpha()
        }

        self.animation = {
            'projectile1': Animation(self.getImg("projectileSheet"),8,8,0,60,0.001,True),
            'projectile2': Animation(self.getImg("projectileSheet2"), 1, 5, 0, 4, 1, True),
            'explosion1': Animation(self.getImg("explosionSheet1"), 10, 10, 0, 18, 0.01, False),
            'explosion2': Animation(self.getImg("explosionSheet2"), 1, 9, 0, 8, 0.1, False)
        }

    def getImg(self, key):
        return self.images[key]

    def getAnimation(self, key):
        return self.animation[key]


mAssets = MAssets()
