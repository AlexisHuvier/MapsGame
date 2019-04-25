from pyengine.Components import PositionComponent


class Behaviour:
    def __init__(self):
        self.game = None
        self.value = None

    def giveparam(self, game, value):
        self.game = game
        self.value = value


class BreakOnTouch(Behaviour):
    def __init__(self):
        super(BreakOnTouch, self).__init__()

    def run(self, bloc):
        self.game.map.deleteblock(bloc.get_component(PositionComponent).get_position())


class WinOnTouch(Behaviour):
    def __init__(self):
        super(WinOnTouch, self).__init__()

    def run(self, bloc):
        self.game.win()


class LooseOnTouch(Behaviour):
    def __init__(self):
        super(LooseOnTouch, self).__init__()

    def run(self, bloc):
        self.game.loose()


class IncreaseScoreOnTouch(Behaviour):
    def __init__(self):
        super(IncreaseScoreOnTouch, self).__init__()

    def run(self, bloc):
        self.game.player.update_score(self.game.player.score + int(self.value))


class DecreaseScoreOnTouch(Behaviour):
    def __init__(self):
        super(DecreaseScoreOnTouch, self).__init__()

    def run(self, bloc):
        self.game.player.update_score(self.game.player.score - int(self.value))


class IncreaseLifeOnTouch(Behaviour):
    def __init__(self):
        super(IncreaseLifeOnTouch, self).__init__()

    def run(self, bloc):
        self.game.player.update_life(self.game.player.life + int(self.value))


class DecreaseLifeOnTouch(Behaviour):
    def __init__(self):
        super(DecreaseLifeOnTouch, self).__init__()

    def run(self, bloc):
        self.game.player.update_life(self.game.player.life - int(self.value))

