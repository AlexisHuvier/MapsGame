import pygame
from pygame import locals as const

from Core.Map import Map
from Core.Block import ListBlockTypes
from Core.Player import Player


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 480))
        self.clock = pygame.time.Clock()
        self.done = True
        self.controles = {
            "GAUCHE": const.K_LEFT,
            "DROITE": const.K_RIGHT,
            "QUIT": const.K_ESCAPE,
            "JUMP": const.K_UP
        }

        self.blocklist = ListBlockTypes()
        self.blocklist.createbasicblocks()

        self.map = Map()
        self.createmap()

        self.player = Player(self)
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

        self.font = pygame.font.SysFont("monospace", 15)
        self.playerpos = self.font.render(str(self.player.getmappos()[0])+" - "+str(self.player.getmappos()[1]), 1,
                                          (255, 255, 0))

        pygame.key.set_repeat(400, 30)

        self.launch()

    def launch(self):
        while self.done:
            for event in pygame.event.get():
                self.process_event(event)

            self.player.update()
            self.update()
        pygame.quit()

    def process_event(self, event):
        if event.type == const.KEYDOWN:
            if event.key == self.controles["QUIT"]:
                self.done = False
            if event.key == self.controles["GAUCHE"]:
                self.player.move(0)
            if event.key == self.controles["DROITE"]:
                self.player.move(1)
            if event.key == self.controles["JUMP"]:
                self.player.jump()
        if event.type == const.QUIT:
            self.done = False

    def update(self):
        try:
            self.screen.fill((0, 0, 0))
            self.clock.tick(60)

            self.map.blocks.draw(self.screen)
            self.player_list.draw(self.screen)
            self.playerpos = self.font.render(str(self.player.getmappos()[0]) + " - " + str(self.player.getmappos()[1]),
                                              1, (255, 255, 0))
            self.screen.blit(self.playerpos, (10, 10))

            pygame.display.update()
        except pygame.error:
            self.done = False

    def createmap(self):
        for i in range(0, 26):
            self.map.createblock(self.blocklist.get(0), [i, 10])
        self.map.createblock(self.blocklist.get(0), [10, 9])
