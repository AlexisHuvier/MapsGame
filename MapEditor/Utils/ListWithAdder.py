from tkinter import Frame, Listbox, StringVar, Button, Toplevel, Label, Entry, OptionMenu
from tkinter.messagebox import showerror


class ListWithAdder(Frame):
    def __init__(self, parent=None, texts=None, font=None, liste=None, double=False, selectmode="single",
                 typewanted="string", listecanadded=None):
        super(ListWithAdder, self).__init__(parent)

        self.namefen = None  # Respect PEP8
        self.nameentry = None  # Respect PEP8
        self.select = None  # Respect PEP8
        self.valueentry = None  # Respect PEP8

        if texts is None:
            texts = ["", "", ""]
        if liste is None:
            liste = []

        self.double = double
        self.liste = liste
        self.listvar = StringVar()
        self.texts = texts
        self.typewanted = typewanted
        self.listecanadded = listecanadded

        self.listvar.set(" ".join(self.liste))
        if font is None:
            self.listwidget = Listbox(self, listvariable=self.listvar, selectmode=selectmode, height=5, width=25)
            self.addbutton = Button(self, text="Ajouter", command=self.addelement)
            self.deletebutton = Button(self, text="Supprimer", command=self.deleteelement)
        else:
            self.listwidget = Listbox(self, listvariable=self.listvar, selectmode=selectmode, font=font, height=5,
                                      width=25)
            self.addbutton = Button(self, text="Ajouter", font=font, command=self.addelement)
            self.deletebutton = Button(self, text="Supprimer", font=font, command=self.deleteelement)
        self.listwidget.grid(row=1, column=1, columnspan=2)
        self.addbutton.grid(row=2, column=1, pady=5)
        self.deletebutton.grid(row=2, column=2, pady=5)

    def updatelist(self, liste):
        self.listwidget.delete(0, "end")
        for i in liste:
            self.listwidget.insert("end", i)

    def deleteelement(self):
        for i in self.listwidget.curselection():
            self.listwidget.delete(i)

    def addelement(self):
        self.namefen = Toplevel()

        namelabel = Label(self.namefen, text=self.texts[0], font=("Arial", 12))

        if self.typewanted == "string":
            self.nameentry = Entry(self.namefen)
            entrybutton = Button(self.namefen, text="Valider", font=("Arial", 12),
                                 command=self.validatestring)
            valuelabel = None  # Respect PEP8
        elif self.typewanted == "sprites":
            if len(self.listecanadded):
                self.select = StringVar()
                self.select.set(self.listecanadded[0])
                self.nameentry = OptionMenu(self.namefen, self.select, *self.listecanadded)
                entrybutton = Button(self.namefen, text="Valider", font=("Arial", 12),
                                     command=self.validatesprite)
            else:
                showerror(self.texts[3], self.texts[4])
                self.namefen.destroy()
                return
            valuelabel = None  # Respect PEP8
        elif self.typewanted == "behaviour":
            if len(self.listecanadded):
                self.select = StringVar()
                self.select.set(self.listecanadded[0])
                self.nameentry = OptionMenu(self.namefen, self.select, *self.listecanadded)
                valuelabel = Label(self.namefen, text="Valeur :", font=("Arial", 12))
                self.valueentry = Entry(self.namefen)
                entrybutton = Button(self.namefen, text="Valider", font=("Arial", 12),
                                     command=self.validatebehaviour)
            else:
                showerror(self.texts[3], self.texts[4])
                self.namefen.destroy()
                return
        else:
            valuelabel = None  # Respect PEP8
            entrybutton = None  # Respect PEP8
        cancelbutton = Button(self.namefen, text="Annuler", font=("Arial", 12), command=self.namefen.destroy)

        namelabel.grid(row=1, column=1, columnspan=2, padx=20, pady=10)
        self.nameentry.grid(row=2, column=1, columnspan=2, padx=20, pady=0)
        if self.typewanted == "behaviour":
            valuelabel.grid(row=3, column=1, padx=5, pady=10)
            self.valueentry.grid(row=3, column=2, padx=5, pady=10)
            entrybutton.grid(row=4, column=1, padx=10, pady=10)
            cancelbutton.grid(row=4, column=2, padx=10, pady=10)
        else:
            entrybutton.grid(row=3, column=1, padx=10, pady=10)
            cancelbutton.grid(row=3, column=2, padx=10, pady=10)

        self.namefen.mainloop()

    def validatestring(self):
        value = self.nameentry.get()
        if value in self.listvar.get() and not self.double:
            showerror(self.texts[1], self.texts[2])
        else:
            self.listwidget.insert("end", value)
            self.namefen.destroy()

    def validatesprite(self):
        value = self.select.get()
        if value in self.listvar.get() and not self.double:
            showerror(self.texts[1], self.texts[2])
        else:
            self.listwidget.insert("end", value)
            self.namefen.destroy()

    def validatebehaviour(self):
        value = self.select.get() + " - " + self.valueentry.get()
        if value in self.listvar.get() and not self.double:
            showerror(self.texts[1], self.texts[2])
        else:
            self.listwidget.insert("end", value)
            self.namefen.destroy()

    def get(self):
        liste = []
        for i in self.listwidget.curselection():
            liste.append(self.listwidget.get(i))
        return liste

    def getall(self):
        liste = []
        for i in self.listwidget.get(0, "end"):
            if i != "":
                liste.append(i)
        return liste
