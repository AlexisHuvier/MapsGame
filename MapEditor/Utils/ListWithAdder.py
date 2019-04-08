from tkinter import Frame, Listbox, StringVar, Button, Toplevel, Label, Entry
from tkinter.messagebox import showerror


class ListWithAdder(Frame):
    def __init__(self, parent=None, texts=None, font=None, liste=None, double=False, selectmode="single"):
        super(ListWithAdder, self).__init__(parent)

        self.namefen = None  # Respect PEP8
        self.nameentry = None  # Respect PEP8

        if texts is None:
            texts = ["", "", ""]
        if liste is None:
            liste = []

        self.double = double
        self.liste = liste
        self.listvar = StringVar()
        self.texts = texts

        self.listvar.set(" ".join(self.liste))
        if font is None:
            self.listwidget = Listbox(self, listvariable=self.listvar, selectmode=selectmode, height=5)
            self.addbutton = Button(self, text="Ajouter", command=self.addelement)
            self.deletebutton = Button(self, text="Supprimer", command=self.deleteelement)
        else:
            self.listwidget = Listbox(self, listvariable=self.listvar, selectmode=selectmode, font=font, height=5)
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
        self.nameentry = Entry(self.namefen)
        entrybutton = Button(self.namefen, text="Valider", font=("Arial", 12),
                             command=self.validatename)
        cancelbutton = Button(self.namefen, text="Annuler", font=("Arial", 12), command=self.namefen.destroy)

        namelabel.grid(row=1, column=1, columnspan=2, padx=20, pady=10)
        self.nameentry.grid(row=2, column=1, columnspan=2, padx=20, pady=0)
        entrybutton.grid(row=3, column=1, padx=10, pady=10)
        cancelbutton.grid(row=3, column=2, padx=10, pady=10)

        self.namefen.mainloop()

    def validatename(self):
        value = self.nameentry.get()
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
