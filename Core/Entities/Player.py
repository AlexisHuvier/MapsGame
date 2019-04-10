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
            booldroite = not self.game.map.getblockfrompos([self.getmappos()[0]+1, self.getmappos()[1]]).solid
            boolgauche = False
        else:
            booldroite = False
            boolgauche = not self.game.map.getblockfrompos(self.getmappos()).solid

        if booldroite:
            if self.rect.x + self.speed >= 800 - 32:
                self.rect.x = 800 - 32
            else:
                self.rect.x += self.speed
        if boolgauche:
            if self.rect.x - self.speed <= 0:
                self.rect.x = 0
            else:
                self.rect.x -= self.speed

    def jump(self):
        if self.grounded and not self.game.map.getblockfrompos([self.getmappos()[0], self.getmappos()[1]-1]).solid \
                and not self.game.map.getblockfrompos([self.getmappos()[0]+1, self.getmappos()[1]-1]).solid:
            self.gravity = -5
            self.grounded = False

    def update(self):
        super(Player, self).update()

        if self.rect.y > 480:
            if self.game.map.looseonfall:
                self.game.loose()
            else:
                self.rect.y = 0
