import pygame as pg #pygame is a free and open source external library for game development in python
import math
from spaceBodies import CelestialBody

class Planet(CelestialBody):

    green = (0, 255, 0)
    
    def __init__(self, position, size = None, velocity = None, acceleration = None, theta = None, mass = None, radius = None):
        super(Planet, self).__init__(position = position, size = size, velocity = velocity, acceleration = acceleration, theta = theta, mass = mass)
        self.radius = radius

    def touching_ship(ship):
        for v in ship.get_vertices():
            if math.sqrt((v[0]-self.position[0])**2 + (v[1]-self.position[1])**2) <= self.radius:
                return True
        return False

    def draw(self, screen):
        pg.draw.circle(screen, self.green, self.position, self.radius)
