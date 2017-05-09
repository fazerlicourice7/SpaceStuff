import pygame as pg
from spaceBodies import CelestialBody


class Projectile(CelestialBody):

    LENGTH = 4
    MULTIPLIER = 2 
    
    def __init__(self, position, velocity, color):
        self.position = position
        self.velocity = (self.MULTIPLIER*velocity[0], -self.MULTIPLIER*velocity[1])
        self.color = color

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def hit_ship(self, ship):
        vertices = ship.get_vertices()
        xVertices = []
        yVertices = []
        for v in vertices:
            xVertices.append(v[0])
            yVertices.append(v[1])
        left = min(xVertices)
        right = max(xVertices)
        top = min(yVertices)
        bottom = max(yVertices)

        p = self.position
        if(p[0] > left and p[0] < right and p[1] > top and p[1] < bottom):
            return True
        return False

    def draw(self, screen):
        self.update()
        end_point = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        pg.draw.line(screen, self.color, self.position, end_point, 4)
