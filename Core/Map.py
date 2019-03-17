import pygame

from Core.Block import Block


class Map:
    def __init__(self):
        self.blocks = pygame.sprite.Group()

    def createblock(self, typeblock, pos):
        block = Block(typeblock, pos)
        self.blocks.add(block)

    def getblockfrompos(self, pos):
        for i in self.blocks.sprites():
            if i.getpos()[0] == pos[0] and i.getpos()[1] == pos[1]:
                return i.blocktype.name
        return "air"

