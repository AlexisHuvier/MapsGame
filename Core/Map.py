import json

from Core.Entities.Block import Block
from Core.Entities.Block import BlockType

from pyengine.Components import PositionComponent


class Map:
    def __init__(self, game, directory, entitysystem):
        self.game = game
        self.directory = directory
        self.entitySystem = entitysystem

        with open(directory+"/map.json", 'r') as f:
            datas = json.load(f)
        self.name = datas["name"]
        self.description = datas["description"]
        self.author = datas["author"]
        self.scoretowin = int(datas["scoreToWin"])
        self.looseonfall = bool(datas["looseOnFall"])
        for i in datas["blocks"]:
            self.createblock(self.game.blocklist.get(i["id"]), [i["x"], i["y"]])

    def createblock(self, typeblock, pos):
        block = Block(typeblock, pos)
        self.entitySystem.add_entity(block)

    def deleteblock(self, pos):
        for i in self.entitySystem.entities.sprites():
            component = i.get_component(PositionComponent)
            if component.get_position()[0] == pos[0] and component.get_position()[1] == pos[1]:
                self.entitySystem.entities.remove(i)

    def getblockfrompos(self, pos):
        for i in self.entitySystem.entities.sprites():
            component = i.get_component(PositionComponent)
            if component.get_position()[0] == pos[0] and component.get_position()[1] == pos[1]:
                return i.blocktype
        return BlockType(self.game, "", "air", -1, False, [])

