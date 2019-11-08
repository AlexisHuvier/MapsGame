from Core.Common.BasicBlock import BasicBlock, BasicBlockType
from pyengine2.Components import CollisionComponent

from Core.Game.Behaviors import *


class BlockType(BasicBlockType):
    behaviors_func = {
        "LooseOnTouch": looseOnTouch,
        "WinOnTouch": winOnTouch
    }

    def __init__(self, game, directory, sprites, name, idblock, solid, behaviors=None):
        super(BlockType, self).__init__(directory, sprites, name, idblock, solid)
        self.game = game
        if behaviors is None:
            behaviors = []
        self.behaviors = {}
        for i in behaviors:
            if len(i.split(" ")) >= 2:
                behaviour = i.split(" ")[0]
                self.behaviors[behaviour] = i.split(" ")[1:]
            else:
                behaviour = i
                self.behaviors[behaviour] = []

            if i in ("LooseOnTouch", "WinOnTouch"):
                self.behaviors[behaviour].append(self.game)

    def launch(self, type_):
        for k, v in self.behaviors.items():
            if type_ in k:
                self.behaviors_func[k](*v)


class Block(BasicBlock):
    def __init__(self, blocktype, x, y):
        super(Block, self).__init__(blocktype, x, y)
        if blocktype.solid:
            self.add_component(CollisionComponent())
        else:
            self.add_component(CollisionComponent(solid=False))
