from pyengine2 import World

from pyengine2.Widgets import Label, Button, Entry
from pyengine2.Utils import Font, Color


class MenuPrincipal(World):
    def __init__(self, window):
        super(MenuPrincipal, self).__init__(window)

        title_font = Font(size=25)
        title_size = title_font.rendered_size("MapsGame")
        self.title = Label(window.width / 2 - title_size[0] / 2, 40, "MapsGame", title_font)

        self.map_name = Entry(window.width / 2 - 100, 200, font=Font(color=Color.from_name("BLACK"), size=18))
        self.map_name.text = "BasicMap"
        self.map_name.update_render()

        self.edit = Button(window.width / 3 - 50, 300, "Editer", lambda: print())
        self.play = Button(2 * window.width / 3 - 50, 300, "Jouer", self.play_fnc)

        self.ui_system.add_widget(self.title)
        self.ui_system.add_widget(self.map_name)
        self.ui_system.add_widget(self.edit)
        self.ui_system.add_widget(self.play)

    def play_fnc(self):
        if len(self.map_name.text):
            self.window.worlds[1].setup(self.map_name.text)
            self.window.set_world(1)
