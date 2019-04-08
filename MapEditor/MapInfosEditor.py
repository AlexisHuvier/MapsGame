from tkinter import Tk, Label, Entry, Checkbutton, Button, Text, IntVar
import json
from tkinter.messagebox import showerror


class MapInfosEditor:
    def __init__(self, mapdir):
        self.mapdir = mapdir
        with open("maps/"+mapdir+"/map.json", "r") as f:
            self.mapinfos = json.load(f)

        self.fenetre = Tk()
        self.fenetre.title("MapsGame")
        self.fenetre.resizable(False, False)
        self.fenetre.geometry("550x550")

        self.fonts = {
            "title": ("Arial", 19, 'bold'),
            "other": ("Arial", 13)
        }

        titre = Label(self.fenetre, text="Editeur MapInfos", font=self.fonts["title"])
        name = Label(self.fenetre, text="Nom :", font=self.fonts["other"])
        self.nameentry = Entry(self.fenetre, font=self.fonts["other"], width=15)
        self.nameentry.insert(0, self.mapinfos["name"])
        description = Label(self.fenetre, text="Description :", font=self.fonts["other"])
        self.descriptiontext = Text(self.fenetre, font=self.fonts["other"], height=10, width=30)
        self.descriptiontext.insert("1.0", self.mapinfos["description"])
        author = Label(self.fenetre, text="Auteur :", font=self.fonts["other"])
        self.authorentry = Entry(self.fenetre, font=self.fonts["other"], width=15)
        self.authorentry.insert(0, self.mapinfos["author"])
        score = Label(self.fenetre, text="Score pour gagner :", font=self.fonts["other"])
        vcmd = (self.fenetre.register(self.validateint),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.scoreentry = Entry(self.fenetre, validate='key', validatecommand=vcmd, font=self.fonts["other"], width=15)
        self.scoreentry.insert(0, self.mapinfos["scoreToWin"])
        self.loose = IntVar()
        self.looseentry = Checkbutton(self.fenetre, font=self.fonts["other"], text="Tomber = Perdu",
                                      variable=self.loose)
        if self.mapinfos["looseOnFall"]:
            self.looseentry.select()
        savebutton = Button(self.fenetre, text="Sauvegarder", font=self.fonts["other"], command=self.save)
        exitbutton = Button(self.fenetre, text="Retour Editeur", font=self.fonts["other"], command=self.returntoeditor)

        self.fenetre.columnconfigure(0, weight=1)
        self.fenetre.columnconfigure(1, weight=1)

        titre.grid(row=0, column=0, columnspan=2, pady=20)
        name.grid(row=1, column=0, pady=10, padx=10, sticky="E")
        self.nameentry.grid(row=1, column=1, pady=10, padx=10, sticky="W")
        description.grid(row=2, column=0, columnspan=2, pady=2)
        self.descriptiontext.grid(row=3, column=0, columnspan=2, pady=2)
        author.grid(row=4, column=0, pady=10, padx=10, sticky="E")
        self.authorentry.grid(row=4, column=1, pady=10, padx=10, sticky="W")
        score.grid(row=5, column=0, pady=10, padx=10, sticky="E")
        self.scoreentry.grid(row=5, column=1, pady=10, padx=10, sticky="W")
        self.looseentry.grid(row=6, column=0, pady=10, columnspan=2)
        savebutton.grid(row=7, column=0, pady=10, padx=10, sticky="E")
        exitbutton.grid(row=7, column=1, padx=10, pady=10, sticky="W")

        self.fenetre.mainloop()

    def returntoeditor(self):
        from MapEditor.Editor import Editor

        self.fenetre.destroy()
        Editor(self.mapdir)

    def save(self):
        self.mapinfos["name"] = self.nameentry.get()
        self.mapinfos["description"] = self.descriptiontext.get("1.0", "end")
        self.mapinfos["author"] = self.authorentry.get()
        try:
            self.mapinfos["scoreToWin"] = int(self.scoreentry.get())
        except ValueError:
            showerror("Score Invalide", "Le score entré n'est pas valide, il n'est pas sauvegardé.")
        self.mapinfos["looseOnFall"] = bool(self.loose.get())
        with open("maps/" + self.mapdir + "/map.json", 'w') as f:
            f.write(json.dumps(self.mapinfos, indent=4))

    def validateint(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if text in "0123456789-+":
            if value_if_allowed == "" or value_if_allowed in ["-", "+"]:
                return True
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
