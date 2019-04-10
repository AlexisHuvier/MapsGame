from Core.Entities.Entity import Entity
import pygame


class LifeBar:
    def __init__(self, game, pos, offset, maxhealth):
        super(LifeBar)
        self.offset = offset
        self.lifeback = Entity(game, [pos[0]+offset[0], pos[1]+offset[1]], "images/lifeback.png", False)
        self.lifefront = Entity(game, [pos[0]+offset[0], pos[1]+offset[1]], "images/lifefront.png", False)
        self.maxhealth = maxhealth
        self.maxwidth = self.lifefront.image.get_width()

    def updatelife(self, health):
        newwidth = int(health*self.maxwidth/self.maxhealth)
        self.lifefront.image = pygame.transform.scale(self.lifefront.image, (newwidth,
                                                                             self.lifefront.image.get_height()))

    def updatepos(self, pos):
        self.lifeback.updatepos([pos[0]+self.offset[0], pos[1]+self.offset[1]])
        self.lifefront.updatepos([pos[0]+self.offset[0], pos[1]+self.offset[1]])
