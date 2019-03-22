import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Player, self).__init__()
        self.game = game
        self.imagestr = "images/player.png"
        self.image = pygame.image.load(self.imagestr)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        self.gravity = 5
        self.timegravity = 5
        self.speed = 3
        self.grounded = False

    def getpos(self):
        return self.rect.x, self.rect.y

    def getmappos(self):
        return int(self.rect.x/32), int(self.rect.y/32)

    def move(self, direction):
        if direction:
            booldroite = not self.game.map.getblockfrompos([self.getmappos()[0]+1, self.getmappos()[1]]).solid
            boolgauche = False
        else:
            booldroite = False
            boolgauche = not self.game.map.getblockfrompos(self.getmappos()).solid

        if booldroite:
            self.rect.x += self.speed
        if boolgauche:
            self.rect.x -= self.speed

    def jump(self):
        if self.grounded and not self.game.map.getblockfrompos([self.getmappos()[0], self.getmappos()[1]-1]).solid \
                and not self.game.map.getblockfrompos([self.getmappos()[0]+1, self.getmappos()[1]-1]).solid:
            self.gravity = -5
            self.grounded = False

    def update(self):
        if not self.grounded:
            self.rect.y += self.gravity
        elif self.gravity < 0:
            self.rect.y += self.gravity
        else:
            self.gravity = 2
        self.grounded = False

        if self.timegravity <= 0 and self.gravity < 5 and not self.grounded:
            self.gravity += 1
            self.timegravity = 5
        self.timegravity -= 1

        if self.game.map.getblockfrompos([self.getmappos()[0], self.getmappos()[1]+1]).solid \
                or self.game.map.getblockfrompos([self.getmappos()[0]+1, self.getmappos()[1]+1]).solid:
            self.grounded = True

        if self.rect.y > 480:
            self.rect.y = 0
