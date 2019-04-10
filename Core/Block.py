import pygame
import json
import importlib

from Core.Behaviours import IncreaseLifeOnTouch, IncreaseScoreOnTouch, DecreaseLifeOnTouch, DecreaseScoreOnTouch
from Core.Behaviours import BreakOnTouch, WinOnTouch, LooseOnTouch


class BlockType:
    def __init__(self, game, sprites, name, idblock, solid, behaviours):
        self.game = game
        self.sprites = sprites
        self.nbsprites = len(sprites)
        self.name = name
        self.idblock = idblock
        self.solid = solid
        self.behaviours = []
        for i in behaviours["liste"]:
            try:
                behaviour = eval(i+"()")
            except NameError:
                lib = importlib.import_module("maps."+game.mapdir.replace("/", ".")+".Behaviours."+i)
                behaviour = lib.behaviour
            try:
                behaviour.giveparam(game, behaviours[i])
            except KeyError:
                behaviour.giveparam(game, None)
            self.behaviours.append(behaviour)


class ListBlockTypes:
    def __init__(self, game):
        self.dico = {}
        self.game = game

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
            for j in range(len(i["sprites"])):
                i["sprites"][j] = directory + "/" + i["sprites"][j]
            blocktype = BlockType(self.game, i["sprites"], i["name"], i["id"], i["solid"], i["behaviour"])
            self.add(blocktype)


class Block(pygame.sprite.Sprite):
    def __init__(self, blocktype, pos):
        super(Block, self).__init__()
        self.blocktype = blocktype
        self.sprite = 0
        self.image = pygame.image.load(self.blocktype.sprites[self.sprite])
        self.timer = 20
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

    def getrealpos(self):
        return self.rect.x, self.rect.y

    def update(self, game):
        if self.timer <= 0:
            self.timer = 20
            self.sprite += 1
            if self.sprite == self.blocktype.nbsprites:
                self.sprite = 0
            self.image = pygame.image.load(self.blocktype.sprites[self.sprite])
            self.rect = self.image.get_rect()
            self.rect.x = self.x * 32
            self.rect.y = self.y * 32
        self.timer -= 1

        playertouching = False
        playergroup = pygame.sprite.Group()
        playergroup.add(game.player)
        playercollision = pygame.sprite.spritecollide(self, playergroup, False, None)
        if len(playercollision):
            playertouching = True

        for i in self.blocktype.behaviours:
            i.run(playertouching, self)
