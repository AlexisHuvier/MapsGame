from tkinter import Tk, Label, Button, StringVar, OptionMenu
import os

from Core.Game import Game


class MenuPrincipal:
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

        game = Game(self.v.get())


if __name__ == '__main__':
    Menu = MenuPrincipal()
