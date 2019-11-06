from pyengine2.Entities import Entity
from pyengine2.Components import PositionComponent, SpriteComponent, ShowComponent


class BasicPlayer(Entity):
    def __init__(self, x, y, sprite="files/player.png"):
        super(BasicPlayer, self).__init__()

        self.add_component(PositionComponent(x, y))
        self.add_component(SpriteComponent("files/player.png"))
        self.add_component(ShowComponent())
