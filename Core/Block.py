import pygame
import json


class BlockType:
    def __init__(self, sprite, name, idblock):
        self.sprite = sprite
        self.name = name
        self.idblock = idblock


class ListBlockTypes:
    def __init__(self):
        self.dico = {}

    def add(self, blocktype):
        if blocktype.idblock in self.dico:
            print("ERREUR : Le bloc d'id", blocktype.id, "existe déjà.")
        else:
            self.dico[blocktype.idblock] = blocktype

    def get(self, idblock):
        for k, v in self.dico.items():
            if idblock == k:
                return v
        print("ERREUR : Il n'existe pas de bloc à l'id", idblock)

    def getall(self):
        return self.dico

    def createblocks(self, directory):
        with open(directory + "/blocks.json", 'r') as f:
            datas = json.load(f)
        for i in datas["types"]:
            blocktype = BlockType(directory + "/" + i["image"], i["name"], i["id"], i["solid"], i["behaviour"])
            self.add(blocktype)


class Block(pygame.sprite.Sprite):
    def __init__(self, blocktype, pos):
        super(Block, self).__init__()
        self.blocktype = blocktype
        self.image = pygame.image.load(self.blocktype.sprite)
        self.rect = self.image.get_rect()
        self.x = pos[0]
        self.y = pos[1]
        self.rect.x = self.x * 32
        self.rect.y = self.y * 32

    def setpos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect.x = self.x * 32
        self.rect.y = self.y * 32

    def getpos(self):
        return self.x, self.y
