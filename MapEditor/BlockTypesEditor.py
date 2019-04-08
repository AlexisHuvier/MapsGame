from tkinter import Tk, Label, Button, OptionMenu, StringVar, Entry, Checkbutton, IntVar, Frame
import json

from MapEditor.Utils.ListWithAdder import ListWithAdder


class BlockTypesEditor:
    def __init__(self, mapdir):
        self.mapdir = mapdir
        with open("maps/" + mapdir + "/blocks.json", 'r') as f:
            datas = json.load(f)
        self.blocktypes = datas["types"]
        self.id = []
        for i in self.blocktypes:
            self.id.append(i["id"])

        self.fenetre = Tk()
        self.fenetre.title("MapsGame")
        self.fenetre.resizable(False, False)
        self.fenetre.geometry("600x550")

        self.fonts = {
            "title": ("Arial", 19, 'bold'),
            "other": ("Arial", 13)
        }

        self.texts = [
            [
                "Lien du sprite",
                "Sprite déjà utilisé",
                "Ce sprite est déjà utilisé pour ce blocktype."
            ],
            [
                "Nom du comportement",
                "Comportement déjà utilisé",
                "Ce comportement est déjà utilisé pour ce blocktype."
            ]
        ]

        titre = Label(self.fenetre, text="Editeur BlockType", font=self.fonts["title"])
        if len(self.id):
            self.idlabel = Label(self.fenetre, text="ID :", font=self.fonts["other"])
            self.v = StringVar()
            self.v.set(self.id[0])
            self.om = OptionMenu(self.fenetre, self.v, *self.id, command=self.update)
            self.om['font'] = self.fonts["other"]
            self.namelabel = Label(self.fenetre, text="Name :", font=self.fonts["other"])
            self.nameentry = Entry(self.fenetre, font=self.fonts["other"], width=15)
            self.nameentry.insert(0, self.blocktypes[0]["name"])
            self.spritelabel = Label(self.fenetre, text="Sprites :", font=self.fonts["other"])
            self.spriteslist = ListWithAdder(self.fenetre, self.texts[0], self.fonts["other"],
                                             self.blocktypes[0]["sprites"])
            self.solidstate = IntVar()
            self.solidentry = Checkbutton(self.fenetre, font=self.fonts["other"], text="Solide",
                                          variable=self.solidstate)
            if self.blocktypes[0]["solid"]:
                self.solidentry.select()
            self.behaviourlabel = Label(self.fenetre, text="Comportements :", font=self.fonts["other"])
            self.behaviourlist = ListWithAdder(self.fenetre, self.texts[1], self.fonts["other"],
                                               self.blocktypes[0]["behaviour"])
            self.boutonframe2 = Frame(self.fenetre)
            self.deletebutton = Button(self.boutonframe2, text="Supprimer", font=self.fonts["other"], command=self.delete)
            self.savebutton = Button(self.boutonframe2, text="Sauvegarder", font=self.fonts["other"], command=self.save)
            self.deletebutton.grid(row=0, column=0, padx=10)
            self.savebutton.grid(row=0, column=1, padx=10)

        self.boutonframe = Frame(self.fenetre)
        self.addbutton = Button(self.boutonframe, text="Ajouter", font=self.fonts["other"], command=self.addblocktype)
        self.exitbutton = Button(self.boutonframe, text="Retour Editeur", font=self.fonts["other"], command=self.returntoeditor)
        self.addbutton.grid(row=0, column=0, padx=10)
        self.exitbutton.grid(row=0, column=1, padx=10)

        self.fenetre.columnconfigure(0, weight=1)
        self.fenetre.columnconfigure(1, weight=1)

        titre.grid(row=1, column=0, columnspan=2, padx=10, pady=20)
        if len(self.id):
            self.idlabel.grid(row=2, column=0, padx=10, pady=10, sticky="E")
            self.om.grid(row=2, column=1, padx=10, pady=10, sticky="W")
            self.namelabel.grid(row=3, column=0, padx=10, pady=15, sticky="E")
            self.nameentry.grid(row=3, column=1, padx=10, pady=15, sticky="W")
            self.spritelabel.grid(row=4, column=0, padx=10, pady=5)
            self.behaviourlabel.grid(row=4, column=1, padx=10, pady=5)
            self.spriteslist.grid(row=5, column=0, padx=10, pady=5)
            self.behaviourlist.grid(row=5, column=1, padx=10, pady=5)
            self.solidentry.grid(row=6, column=0, columnspan=2, padx=10, pady=15)
            self.boutonframe2.grid(row=9, column=0, padx=10, pady=15, sticky="E")
            self.boutonframe.grid(row=9, column=1, padx=10, pady=15, sticky="W")
        else:
            self.boutonframe.grid(row=9, column=0, columnspan=2, padx=10, pady=15)

        self.fenetre.mainloop()

    def update(self, newvalue):
        newtype = self.blocktypes[int(newvalue)]

        self.nameentry.delete(0, len(self.nameentry.get()))
        self.nameentry.insert(0, newtype["name"])
        self.spriteslist.updatelist(newtype["sprites"])
        self.behaviourlist.updatelist(newtype["behaviour"])
        if newtype["solid"]:
            self.solidentry.select()
        else:
            self.solidentry.deselect()

    def delete(self):
        idtodelete = int(self.v.get())
        for i in self.blocktypes:
            if i["id"] > idtodelete:
                i["id"] -= 1
        del self.blocktypes[int(self.v.get())]
        with open("maps/" + self.mapdir + "/blocks.json", 'w') as f:
            f.write(json.dumps({"types": self.blocktypes}, indent=4))
        self.fenetre.destroy()
        self.__init__(self.mapdir)

    def save(self):
        idtoupdate = int(self.v.get())
        for i in self.blocktypes:
            if i["id"] == idtoupdate:
                i["name"] = self.nameentry.get()
                i["sprites"] = self.spriteslist.getall()
                i["behaviour"] = self.behaviourlist.getall()
                i["solid"] = bool(self.solidstate.get())
        with open("maps/" + self.mapdir + "/blocks.json", 'w') as f:
            f.write(json.dumps({"types": self.blocktypes}, indent=4))

    def returntoeditor(self):
        from MapEditor.Editor import Editor

        self.fenetre.destroy()
        Editor(self.mapdir)

    def addblocktype(self):
        self.blocktypes.append({
            "id": len(self.blocktypes),
            "name": "Nom",
            "sprites": [""],
            "solid": True,
            "behaviour": []
        })
        with open("maps/" + self.mapdir + "/blocks.json", 'w') as f:
            f.write(json.dumps({"types": self.blocktypes}, indent=4))
        self.fenetre.destroy()
        self.__init__(self.mapdir)

