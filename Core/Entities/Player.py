from pyengine import Entity
from pyengine.Components import PositionComponent, SpriteComponent, ControlComponent, PhysicsComponent
from pyengine.Enums import ControlType

from Core.Entities.Block import Block


class Player(Entity):
    def __init__(self, game):
        super(Player, self).__init__()
        self.game = game
        self.entitySystem = self.game.entitySystem
        self.add_components(PositionComponent, [0, 0])
        self.add_components(SpriteComponent, "images/player.png")
        self.add_components(PhysicsComponent)
        self.get_component(PhysicsComponent).set_callback(self.collision)
        self.add_components(ControlComponent, ControlType.CLASSICJUMP)
        self.score = 0
        self.life = 100

    @staticmethod
    def collision(objet):
        if type(objet) == Block:
            for i in objet.blocktype.behaviours:
                if "OnTouch" in i.__class__.__name__:
                    i.run(objet)

    def update_score(self, valeur):
        self.score = valeur
        if self.score >= self.game.map.scoretowin:
            self.score = self.game.map.scoretowin
            self.game.win()

    def update_life(self, valeur):
        self.life = valeur
        if self.life <= 0:
            self.life = 0
            self.game.loose()

