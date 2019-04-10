from Core.Entities.Entity import Entity
from Core.Entities.LifeBar import LifeBar


class Player(Entity):
    def __init__(self, game):
        super(Player, self).__init__(game, [10, 10], "images/player.png")
        self.speed = 3
        self.score = 0

    def addscore(self, add):
        if self.score + add >= self.game.map.scoretowin:
            self.score = self.game.map.scoretowin
            self.game.win()
        else:
            self.score += add

    def removescore(self, remove):
        if self.score-remove < 0:
            self.score = 0
        else:
            self.score -= remove

    def updatelife(self, newlife):
        if newlife >= self.maxlife:
            newlife = self.maxlife
        if newlife <= 0:
            self.game.loose()
        self.life = newlife
        self.lifebar.updatelife(newlife)

    def move(self, direction):
        if direction:
            if self.rect.x + self.speed >= 800 - 32:
                if self.cango([800-32, self.rect.y]):
                    self.rect.x = 800 - 32
            else:
                if self.cango([self.rect.x + self.speed, self.rect.y ]):
                    self.rect.x += self.speed
        elif not direction:
            if self.rect.x - self.speed <= 0:
                if self.cango([0, self.rect.y]):
                    self.rect.x = 0
            else:
                if self.cango([self.rect.x - self.speed, self.rect.y]):
                    self.rect.x -= self.speed

    def jump(self):
        if self.grounded:
            self.gravity = -5
            self.grounded = False

    def update(self):
        super(Player, self).update()

        if self.rect.y > 480:
            if self.game.map.looseonfall:
                self.game.loose()
            else:
                self.rect.y = 0

        self.lifebar.updatepos(self.getpos())
