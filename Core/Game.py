import pygame
from pygame import locals as const
from tkinter import Tk, Label, Button, StringVar, OptionMenu
import os

from Core.Map import Map
from Core.Block import ListBlockTypes
from Core.Player import Player


class Game:
    def __init__(self, mapdir):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 480))
        self.clock = pygame.time.Clock()
        self.done = True
        self.state = 0
        self.controles = {
            "GAUCHE": const.K_LEFT,
            "DROITE": const.K_RIGHT,
            "QUIT": const.K_ESCAPE,
            "JUMP": const.K_UP,
            "DEBUG": const.K_d
        }
        self.debug = False

        self.blocklist = ListBlockTypes()
        self.blocklist.createblocks("maps/"+mapdir)

        self.map = Map(self, "maps/"+mapdir)

        self.player = Player(self)
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

        self.debugfont = pygame.font.SysFont("monospace", 15)
        self.winfont = pygame.font.SysFont("monospace", 20)

        pygame.key.set_repeat(1, 1)

        self.launch()

    def launch(self):
        while self.done:
            for event in pygame.event.get():
                self.process_event(event)

            self.player.update()
            for i in self.map.blocks.sprites():
                i.update(self)
            self.update()

        if self.state != 0:
            self.done = True
            self.screen.fill((0, 0, 0))
            if self.state == 1:
                render = self.winfont.render("Bien joué", 1, (255, 255, 255))
            else:
                render = self.winfont.render("Dommage...", 1, (255, 255, 255))
            self.screen.blit(render, (400, 240))
            pygame.display.update()
            while self.done:
                for event in pygame.event.get():
                    self.process_event(event)
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
        if event.type == const.KEYUP:
            if event.key == self.controles["DEBUG"]:
                self.debug = not self.debug
        if event.type == const.QUIT:
            self.done = False

    def update(self):
        try:
            self.screen.fill((0, 0, 0))
            self.clock.tick(60)

            self.map.blocks.draw(self.screen)
            self.player_list.draw(self.screen)
            if self.debug:
                self.showdebug()

            pygame.display.update()
        except pygame.error:
            self.done = False

    def showdebug(self):
        text = [
            "MapPos : " + str(self.player.getmappos()[0])+", "+str(self.player.getmappos()[1]),
            "RealPos : " + str(self.player.getpos()[0])+", "+str(self.player.getpos()[1]),
            "Grounded : "+str(self.player.grounded)
            ]
        y = 10
        for i in text:
            textrendered = self.debugfont.render(i, 1, (255, 255, 0))
            self.screen.blit(textrendered, (10, y))
            y += 15

    def win(self):
        self.done = False
        self.state = 1

    def loose(self):
        self.done = False
        self.state = 2


class MainMenu:
    def __init__(self):
        self.fenetre = Tk()
        self.fenetre.title("MapsGame")

        titre = Label(self.fenetre, text="MapsGame")
        listeoptions = os.listdir("maps")
        self.v = StringVar()
        self.v.set(listeoptions[0])
        om = OptionMenu(self.fenetre, self.v, *listeoptions)
        launchbutton = Button(self.fenetre, text="Jouer", command=self.launchgame)
        exitbutton = Button(self.fenetre, text="Quitter", command=self.fenetre.destroy)

        titre.pack(padx=10, pady=15)
        om.pack(padx=10, pady=10)
        launchbutton.pack(padx=10, pady=5)
        exitbutton.pack(padx=10, pady=10)

        self.fenetre.mainloop()

    def launchgame(self):
        self.fenetre.destroy()

        Game(self.v.get())
