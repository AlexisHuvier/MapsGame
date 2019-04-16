import pygame
from pygame import locals as const
from tkinter import Tk, Label, Button, StringVar, OptionMenu, Entry
from tkinter.messagebox import askyesno
import os
import json

from Core.Map import Map
from Core.Block import ListBlockTypes
from Core.Entities.Player import Player

from MapEditor.Editor import Editor


class Game:
    def __init__(self, mapdir):
        pygame.init()
        self.mapdir = mapdir

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

        self.entity_list = pygame.sprite.Group()
        self.blocklist = ListBlockTypes(self)

        self.player = Player(self)
        self.entity_list.add(self.player)

        self.blocklist.createblocks("maps/"+mapdir)

        self.map = Map(self, "maps/"+mapdir)

        self.debugfont = pygame.font.SysFont("monospace", 15)
        self.scorefont = pygame.font.SysFont("monospace", 17)
        self.winfont = pygame.font.SysFont("monospace", 20)

        pygame.key.set_repeat(1, 1)

        self.launch()

    def launch(self):
        while self.done:
            for event in pygame.event.get():
                self.process_event(event)

            for i in self.entity_list:
                i.update()
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
            score = self.winfont.render("Score : "+str(self.player.score), 1, (255, 255, 255))
            self.screen.blit(score, (400, 265))
            pygame.display.update()
            while self.done:
                for event in pygame.event.get():
                    self.process_event(event)
        pygame.quit()

        MainMenu()

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
            self.entity_list.draw(self.screen)
            textrendered = self.scorefont.render("Score : "+str(self.player.score), 1, (255, 255, 255))
            self.screen.blit(textrendered, (680, 10))
            if self.debug:
                self.showdebug()

            pygame.display.update()
        except pygame.error:
            self.done = False

    def showdebug(self):
        text = [
            "MapPos : " + str(self.player.getmappos()[0])+", "+str(self.player.getmappos()[1]),
            "RealPos : " + str(self.player.getpos()[0])+", "+str(self.player.getpos()[1]),
            "Grounded : "+str(self.player.grounded),
            "Maps Infos : ",
            "    - Name : "+str(self.map.name),
            "    - Description : "+str(self.map.description),
            "    - Author : "+str(self.map.author),
            "    - LooseOnFall : "+str(self.map.looseonfall),
            "    - ScoreToWin : "+str(self.map.scoretowin)
            ]
        y = 10
        for i in text:
            textrendered = self.debugfont.render(i, 1, (255, 255, 0))
            self.screen.blit(textrendered, (10, y))
            y += 15

    def addentity(self, entity):
        self.entity_list.add(entity)

    def win(self):
        self.done = False
        self.state = 1

    def loose(self):
        self.done = False
        self.state = 2


class MainMenu:
    def __init__(self):
        self.namefen = None  # Respect PEP8
        self.nameentry = None  # Respect PEP8

        self.fenetre = Tk()
        self.fenetre.title("MapsGame")
        self.fenetre.resizable(False, False)
        self.fenetre.geometry("200x380")

        self.fonts = {
            "title": ("Arial", 20, 'bold'),
            "namefen": ("Arial", 12),
            "other": ("Arial", 14)
        }

        titre = Label(self.fenetre, text="MapsGame", font=self.fonts["title"])
        listeoptions = os.listdir("maps")
        self.v = StringVar()
        self.v.set(listeoptions[0])
        om = OptionMenu(self.fenetre, self.v, *listeoptions)
        om['font'] = self.fonts["other"]
        launchbutton = Button(self.fenetre, text="Jouer", font=self.fonts["other"], command=self.launchgame)
        editbutton = Button(self.fenetre, text="Editer Map", font=self.fonts["other"], command=self.editmap)
        createbutton = Button(self.fenetre, text="Créer Map", font=self.fonts["other"], command=self.createmap)
        exitbutton = Button(self.fenetre, text="Quitter", font=self.fonts["other"], command=self.fenetre.destroy)

        titre.pack(padx=10, pady=20)
        om.pack(padx=10, pady=10)
        launchbutton.pack(padx=10, pady=5)
        editbutton.pack(padx=10, pady=10)
        createbutton.pack(padx=10, pady=5)
        exitbutton.pack(padx=10, pady=10)

        self.fenetre.mainloop()

    def launchgame(self):
        self.fenetre.destroy()

        Game(self.v.get())

    def editmap(self):
        self.fenetre.destroy()

        Editor(self.v.get())

    def createmap(self):
        self.fenetre.destroy()
        self.namefen = Tk()

        namelabel = Label(self.namefen, text="Nom de la map", font=self.fonts["namefen"])
        self.nameentry = Entry(self.namefen)
        entrybutton = Button(self.namefen, text="Valider", font=self.fonts["namefen"], command=self.validatecreation)
        cancelbutton = Button(self.namefen, text="Annuler", font=self.fonts["namefen"], command=self.cancelcreation)

        namelabel.grid(row=1, column=1, columnspan=2, padx=20, pady=10)
        self.nameentry.grid(row=2, column=1, columnspan=2, padx=20, pady=0)
        entrybutton.grid(row=3, column=1, padx=10, pady=10)
        cancelbutton.grid(row=3, column=2, padx=10, pady=10)

        self.namefen.mainloop()

    def validatecreation(self):

        mapdir = self.nameentry.get()
        if mapdir in os.listdir("maps"):
            if askyesno("Maps Déjà Existante", "La map existe déjà.\nVoulez-vous l'éditer ?"):
                self.namefen.destroy()
                Editor(mapdir)
        else:
            self.namefen.destroy()
            os.mkdir("maps/"+mapdir)
            os.mkdir("maps/"+mapdir+"/Behaviours")
            blocksjson = {
                "types": []
            }
            mapjson = {
                "name": "Nom",
                "description": "Description",
                "author": "Auteur",
                "scoreToWin": -1,
                "looseOnFall": False,
                "blocks": []
            }
            with open("maps/"+mapdir+'/map.json', 'w') as f:
                f.write(json.dumps(mapjson, indent=4))
            with open("maps/"+mapdir+'/blocks.json', 'w') as f:
                f.write(json.dumps(blocksjson, indent=4))
            Editor(mapdir)

    def cancelcreation(self):
        self.namefen.destroy()
        self.__init__()



