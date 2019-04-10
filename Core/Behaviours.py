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

    def run(self, playertouching, bloc):
        if playertouching:
            self.game.map.deleteblock(bloc.getpos())


class WinOnTouch(Behaviour):
    def __init__(self):
        super(WinOnTouch, self).__init__()

    def run(self, playertouching, bloc):
        self.game.win()


class LooseOnTouch(Behaviour):
    def __init__(self):
        super(LooseOnTouch, self).__init__()

    def run(self, playertouching, bloc):
        if playertouching:
            self.game.loose()


class IncreaseScoreOnTouch(Behaviour):
    def __init__(self):
        super(IncreaseScoreOnTouch, self).__init__()

    def run(self, playertouching, bloc):
        if playertouching:
            self.game.player.addscore(int(self.value))


class DecreaseScoreOnTouch(Behaviour):
    def __init__(self):
        super(DecreaseScoreOnTouch, self).__init__()

    def run(self, playertouching, bloc):
        if playertouching:
            self.game.player.removescore(int(self.value))


class IncreaseLifeOnTouch(Behaviour):
    def __init__(self):
        super(IncreaseLifeOnTouch, self).__init__()

    def run(self, playertouching, bloc):
        if playertouching:
            self.game.player.updatelife(self.game.player.life + int(self.value))


class DecreaseLifeOnTouch(Behaviour):
    def __init__(self):
        super(DecreaseLifeOnTouch, self).__init__()

    def run(self, playertouching, bloc):
        if playertouching:
            self.game.player.updatelife(self.game.player.life - int(self.value))

