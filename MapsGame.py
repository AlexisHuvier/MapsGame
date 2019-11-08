import sys

sys.path.insert(0, "D:\\Programmation\\Python\\Projet\\pyengine\\PyEngine-2")

from pyengine2 import Window

from Core.MenuPrincipal import MenuPrincipal
from Core.Game.Game import Game


class MapsGame(Window):
    def __init__(self):
        super(MapsGame, self).__init__(800, 600, title="MapsGame", debug=True)

        self.set_callback("OUTOFWINDOW", self.outofwindow)

        self.worlds = [MenuPrincipal(self), Game(self)]

        self.world = self.worlds[0]
        self.run()

    def set_world(self, identity):
        self.world = self.worlds[identity]

    def outofwindow(self, entity, pos):
        if self.world == self.worlds[1]:
            self.world.outofwindow(entity, pos)


MapsGame()
