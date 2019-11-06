from pyengine2.Entities import Entity
from pyengine2.Components import PositionComponent, SpriteComponent, ShowComponent

from random import randint

import os


class BlockType:
    def __init__(self, directory, sprites, name, idblock, solid):
        self.sprites = sprites
        self.name = name
        self.idblock = idblock
        self.solid = solid
        self.directory = directory


class BasicBlock(Entity):
    def __init__(self, blocktype, x, y):
        super(BasicBlock, self).__init__()
        self.blocktype = blocktype
        self.x = x
        self.y = y
        self.real_x = x * 32
        self.real_y = y * 32
        self.add_component(PositionComponent(self.real_x, self.real_y))
        random = randint(0, len(self.blocktype.sprites)-1)
        self.add_component(SpriteComponent(os.path.join(self.blocktype.directory, self.blocktype.sprites[random])))
        self.add_component(ShowComponent())
