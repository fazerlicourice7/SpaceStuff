import pygame as pg

class Display(object):

    def __init__(self):
        pg.init()
        width = 1280
        height = 650

        self.size = width, height
        
        self.screen = pg.display.set_mode(self.size)
        #self.screen.init()

    def get_screen(self):
        return self.screen

    def get_size(self):
        return self.size
    

