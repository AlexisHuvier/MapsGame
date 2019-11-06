from Core.Common.BasicPlayer import BasicPlayer
from pyengine2.Components import ControlComponent, CollisionComponent


class Player(BasicPlayer):
    def __init__(self, x, y, sprite="files/player.png"):
        super(Player, self).__init__(x, y, sprite)
        self.add_component(ControlComponent("FOURDIRECTION"))
        self.add_component(CollisionComponent(callback=self.collision))

    @staticmethod
    def collision(entity, cause):
        print(cause, entity.identity)

