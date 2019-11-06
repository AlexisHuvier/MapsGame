from pyengine2 import World

from Core.Common.Map import Map


class Game(World):
    def __init__(self, window):
        super(Game, self).__init__(window)

        self.map = None

    def setup(self, directory):
        self.map = Map(self, directory)
