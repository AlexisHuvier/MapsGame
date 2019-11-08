from Core.Common.BasicPlayer import BasicPlayer
from Core.Game.Block import Block
from pyengine2.Components import ControlComponent, CollisionComponent, PhysicsComponent


class Player(BasicPlayer):
    def __init__(self, x, y, sprite="files/player.png"):
        super(Player, self).__init__(x, y, sprite)
        self.add_component(PhysicsComponent())
        self.add_component(ControlComponent("CLASSICJUMP"))
        self.add_component(CollisionComponent(callback=self.collision))

    @staticmethod
    def collision(entity, cause):
        if isinstance(entity, Block):
            entity.blocktype.launch("OnTouch")

