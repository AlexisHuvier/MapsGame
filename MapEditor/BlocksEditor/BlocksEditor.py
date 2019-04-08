import pygame
from pygame import locals as const
import json
from MapEditor.BlocksEditor.Block import Block, BlockType


class BlocksEditor:
    def __init__(self, mapdir):
        self.mapdir = mapdir
        self.id = 0
        self.mousepos=(0, 0)

        pygame.init()

        self.screen = pygame.display.set_mode((800, 480))
        self.clock = pygame.time.Clock()
        self.done = True

        self.blocktypes = self.loadtypes()
        self.blocks = self.loadblocks()

        self.launch()

    def launch(self):
        while self.done:
            for event in pygame.event.get():
                self.process_event(event)

            self.update()
        pygame.quit()
        from MapEditor.Editor import Editor

        Editor(self.mapdir)

    def update(self):
        self.screen.fill((0, 0, 0))
        self.clock.tick(60)

        self.blocks.draw(self.screen)

        for i in self.blocktypes:
            if self.id == i.idblock:
                self.screen.blit(pygame.image.load(i.sprite), (self.mousepos[0]*32, self.mousepos[1]*32))

        render = pygame.font.SysFont("monospace", 15).render("ID : "+str(self.id), 1, (255, 255, 255))
        self.screen.blit(render, (10, 10))

        pygame.display.update()

    def process_event(self, evt):
        if evt.type == const.QUIT:
            self.done = False
        if evt.type == const.MOUSEBUTTONDOWN:
            self.mouseevent(evt.button, evt.pos)
        if evt.type == const.MOUSEMOTION:
            self.mousepos = (evt.pos[0]//32, evt.pos[1]//32)
        if evt.type == const.KEYUP:
            self.keyevent(evt.key)

    def keyevent(self, key):
        if key == const.K_s:
            liste = []
            for i in self.blocks:
                liste.append({
                    "id": i.blocktype.idblock,
                    "x": i.x,
                    "y": i.y
                })
            with open("maps/"+self.mapdir+"/map.json") as f:
                datas = json.load(f)
            datas["blocks"] = liste

            with open("maps/" + self.mapdir + "/map.json", "w") as f:
                f.write(json.dumps(datas, indent=4))
            print("MAP SAVED")

    def mouseevent(self, button, pos):
        if button == 1:
            x = pos[0] // 32
            y = pos[1] // 32
            for i in self.blocks:
                if x == i.x and y == i.y:
                    self.blocks.remove(i)
                    break
            for i in self.blocktypes:
                if self.id == i.idblock:
                    self.blocks.add(Block(i, [x, y]))
        elif button == 4:
            if self.id + 1 == len(self.blocktypes):
                self.id = -1
            else:
                self.id += 1
        elif button == 5:
            if self.id == -1:
                self.id = len(self.blocktypes)-1
            else:
                self.id -= 1

    def loadtypes(self):
        with open("maps/"+self.mapdir+"/blocks.json") as f:
            datas = json.load(f)
        liste = []
        for i in datas["types"]:
            liste.append(BlockType(i["id"], "maps/"+self.mapdir+"/"+i["sprites"][0]))
        return liste

    def loadblocks(self):
        with open("maps/"+self.mapdir+"/map.json") as f:
            datas = json.load(f)
        liste = pygame.sprite.Group()
        for i in datas["blocks"]:
            for j in self.blocktypes:
                if i["id"] == j.idblock:
                    liste.add(Block(j, [i["x"], i["y"]]))
        return liste
