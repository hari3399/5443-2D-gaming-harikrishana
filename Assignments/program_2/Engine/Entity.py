class Entity:

    def __init__(self, pos):
        self.pos = pos
        self.destroy = False

    def update(self):
        pass

    def draw(self):
        pass

    def getRect(self):
        pass

    # def getRect(self):  # get the rectangle box of object
    #     rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())
    #     return rect
