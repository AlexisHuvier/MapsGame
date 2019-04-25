from Core.Behaviours import Behaviour


class IncreaseSpeedOnTouch(Behaviour):
    def __init__(self):
        super(IncreaseSpeedOnTouch, self).__init__()

    def run(self, bloc):
        self.game.player.speed += int(self.value)


behaviour = IncreaseSpeedOnTouch()
