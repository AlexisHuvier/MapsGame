import json
import os

from Core.Game.Player import Player, BasicPlayer
from Core.Game.Block import Block, BasicBlock, BasicBlockType, BlockType

from pyengine2.Components import PositionComponent
from pyengine2.Utils import Vec2


class Map:
    def __init__(self, world, name, editor=False):
        self.directory = os.path.join("maps", name)
        self.world = world

        with open(os.path.join(self.directory, "blocks.json"), "r") as f:
            blocks = json.load(f)

        if editor:
            self.blocktypes = {i["id"]: BasicBlockType(self.directory, i["sprites"], i["name"], i["id"],
                                                       i["solid"]) for i in blocks["types"]}
        else:
            self.blocktypes = {i["id"]: BlockType(self.world, self.directory, i["sprites"], i["name"], i["id"],
                                                  i["solid"], i["behaviors"]) for i in blocks["types"]}

        with open(os.path.join(self.directory, "map.json"), "r") as f:
            self.map = json.load(f)
        self.score_win = int(self.map["scoreToWin"])
        self.loose_fall = bool(self.map["looseOnFall"])

        if editor:
            for i in self.map["blocks"]:
                self.world.entity_system.add_entity(BasicBlock(self.blocktypes.get(i["id"]), i["x"], i["y"]))
        else:
            for i in self.map["blocks"]:
                self.world.entity_system.add_entity(Block(self.blocktypes.get(i["id"]), i["x"], i["y"]))

        if editor:
            if self.map["player"]["sprite"] == "default":
                self.player = BasicPlayer(self.map["player"]["x"], self.map["player"]["y"])
                self.world.entity_system.add_entity(self.player)
            else:
                self.player = BasicPlayer(self.map["player"]["x"], self.map["player"]["y"],
                                          self.map["player"]["sprite"])
                self.world.entity_system.add_entity(self.player)
        else:
            if self.map["player"]["sprite"] == "default":
                self.player = Player(self.map["player"]["x"], self.map["player"]["y"])
                self.world.entity_system.add_entity(self.player)
            else:
                self.player = BasicPlayer(self.map["player"]["x"], self.map["player"]["y"],
                                          self.map["player"]["sprite"])
                self.world.entity_system.add_entity(self.player)

    def reset_player(self):
        self.player.get_component(PositionComponent).set_position(self.map["player"]["x"], self.map["player"]["y"])

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

