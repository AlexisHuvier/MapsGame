import pygame
import json

from Core.Block import Block
from Core.Block import BlockType


class Map:
    def __init__(self, game, directory):
        self.game = game
        self.directory = directory
        self.blocks = pygame.sprite.Group()

        with open(directory+"/map.json", 'r') as f:
            datas = json.load(f)
        for i in datas["blocks"]:
            self.createblock(self.game.blocklist.get(i["id"]), [i["x"], i["y"]])

    def createblock(self, typeblock, pos):
        block = Block(typeblock, pos)
        self.blocks.add(block)

    def getblockfrompos(self, pos):
        for i in self.blocks.sprites():
            if i.getpos()[0] == pos[0] and i.getpos()[1] == pos[1]:
                return i.blocktype
        return BlockType("", "air", -1, False, [])

