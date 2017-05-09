import pygame as pg #pygame is a free and open source external library for game development in python

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
    

