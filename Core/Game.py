from pyengine import Window, World
from pyengine.Systems import EntitySystem
from Core.Entities.Player import Player
from Core.Map import Map
from Core.Entities.Block import ListBlockTypes

from tkinter import Tk, Label, Button, StringVar, OptionMenu, Entry
from tkinter.messagebox import askyesno
import os
import json

from MapEditor.Editor import Editor


class Game:
    def __init__(self, mapdir):
        self.mapdir = mapdir

        self.game = Window(800, 480, True)
        self.world = World()
        self.game.set_world(self.world)

        self.entitySystem = self.world.get_system(EntitySystem)
        self.player = Player(self.entitySystem)
        self.entitySystem.add_entity(self.player)

        self.blocklist = ListBlockTypes(self)
        self.blocklist.createblocks("maps/"+mapdir)
        self.map = Map(self, "maps/"+mapdir, self.entitySystem)

        self.game.run()

    def loose(self):
        self.game.stop()

    def win(self):
        self.game.stop()


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



