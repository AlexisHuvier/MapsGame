from Core.Common.BasicBlock import BasicBlock
from pyengine2.Components import CollisionComponent


class Block(BasicBlock):
    def __init__(self, blocktype, x, y):
        super(Block, self).__init__(blocktype, x, y)
        if blocktype.solid:
            self.add_component(CollisionComponent())
        else:
            self.add_component(CollisionComponent(solid=False))
