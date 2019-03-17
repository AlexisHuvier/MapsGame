from tkinter import Tk, Label, Button

from Core.Game import Game


class MenuPrincipal:
    def __init__(self):
        self.fenetre = Tk()
        self.fenetre.title("MapsGame")

        titre = Label(self.fenetre, text="MapsGame")
        launchbutton = Button(self.fenetre, text="Jouer", command=self.launchGame)
        exitbutton = Button(self.fenetre, text="Quitter", command=self.fenetre.destroy)

        titre.pack(padx=10, pady=20)
        launchbutton.pack(padx=10, pady=0)
        exitbutton.pack(padx=10, pady=10)

        self.fenetre.mainloop()

    def launchGame(self):
        self.fenetre.destroy()
        game = Game()


Menu = MenuPrincipal()
