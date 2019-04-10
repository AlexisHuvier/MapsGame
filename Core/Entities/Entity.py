import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, game, pos, image, havephysics = True):
        super(Entity, self).__init__()
        self.game = game
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.timegravity = 5
        self.gravity = 5
        self.grounded = False
        self.havephysics = havephysics

    def update(self):
        if self.havephysics:
            self.updatephysics()

    def updatepos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def getpos(self):
        return self.rect.x, self.rect.y

    def getmappos(self):
        return int(self.rect.x/32), int(self.rect.y/32)

    def cango(self, pos):
        gosprite = pygame.sprite.Sprite()
            if self.cango([self.rect.x, self.rect.y + self.gravity]):
                self.rect.y += self.gravity
        elif self.gravity < 0:
            if self.cango([self.rect.x, self.rect.y + self.gravity]):
                self.rect.y += self.gravity
        else:
            self.gravity = 2

        self.grounded = False
        if not self.cango([self.rect.x, self.rect.y + self.gravity]):
            self.grounded = True
        if self.timegravity <= 0 and self.gravity < 5 and not self.grounded:
            self.gravity += 1
            self.timegravity = 5
        self.timegravity -= 1


