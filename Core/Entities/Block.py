from pyengine import Entity
from pyengine.Components import PositionComponent, SpriteComponent, PhysicsComponent
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

    getall = lambda : return self.dico

    def createblocks(self, directory):
        with open(directory + "/blocks.json", 'r') as f:
            datas = json.load(f)
        for i in datas["types"]:
            for j in range(len(i["sprites"])):
                i["sprites"][j] = directory + "/" + i["sprites"][j]
            blocktype = BlockType(self.game, i["sprites"], i["name"], i["id"], i["solid"], i["behaviour"])
            self.add(blocktype)


class Block(Entity):
    def __init__(self, blocktype, pos):
        super(Block, self).__init__()
        self.blocktype = blocktype
        self.pos = [pos[0]*32, pos[1]*32]
        self.sprite = 0
        self.timer = 20
        self.add_components(PositionComponent, self.pos)
        self.add_components(SpriteComponent, self.blocktype.sprites[0])
        if blocktype.solid:
            self.add_components(PhysicsComponent, False)

