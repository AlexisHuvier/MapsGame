import json
import os

from Core.Game.Player import Player, BasicPlayer
from Core.Game.Block import Block, BasicBlock
from Core.Common.BasicBlock import BlockType

from pyengine2.Components import PositionComponent
from pyengine2.Utils import Vec2


class Map:
    def __init__(self, world, name, editor=False):
        self.directory = os.path.join("maps", name)
        self.world = world

        with open(os.path.join(self.directory, "blocks.json"), "r") as f:
            blocks = json.load(f)

        self.blocktypes = {i["id"]: BlockType(self.directory, i["sprites"], i["name"], i["id"],
                                              i["solid"]) for i in blocks["types"]}

        with open(os.path.join(self.directory, "map.json"), "r") as f:
            map = json.load(f)
        self.score_win = int(map["scoreToWin"])
        self.loose_fall = bool(map["looseOnFall"])

        if editor:
            for i in map["blocks"]:
                self.world.entity_system.add_entity(BasicBlock(self.blocktypes.get(i["id"]), i["x"], i["y"]))
        else:
            for i in map["blocks"]:
                self.world.entity_system.add_entity(Block(self.blocktypes.get(i["id"]), i["x"], i["y"]))

        if editor:
            if map["player"]["sprite"] == "default":
                self.world.entity_system.add_entity(BasicPlayer(map["player"]["x"], map["player"]["y"]))
            else:
                self.world.entity_system.add_entity(BasicPlayer(map["player"]["x"], map["player"]["y"],
                                                                map["player"]["sprite"]))
        else:
            if map["player"]["sprite"] == "default":
                self.world.entity_system.add_entity(Player(map["player"]["x"], map["player"]["y"]))
            else:
                self.world.entity_system.add_entity(Player(map["player"]["x"], map["player"]["y"],
                                                           map["player"]["sprite"]))

    def delete_block(self, x, y):
        for i in self.world.entity_system.entities:
            if i.has_component(PositionComponent):
                if i.get_component(PositionComponent).position() == Vec2(x, y):
                    self.world.entity_system.remove_entity(i)
                    break

    def get_block(self, x, y):
        for i in self.world.entity_system.entities:
            if i.has_component(PositionComponent):
                if i.get_component(PositionComponent).position() == Vec2(x, y):
                    return i.blocktype
        return BlockType("", "air", -1, False)

