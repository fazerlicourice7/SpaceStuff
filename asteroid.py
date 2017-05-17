import pygame as pg
from spaceBodies import CelestialBody
import math, random as r

class Asteroid(CelestialBody):

    MASS = 1000 # adjust depending on size

    def __init__(self, position = None, size = None, velocity = None, acceleration = None, theta = None, mass = None):
        super(Asteroid, self).__init__(position = position, size = size, velocity = velocity, acceleration = acceleration, theta = theta, mass = self.MASS * size)
        self.num_vertices = r.randint(10) + 10
        self.thetas = []
        self.dists = []
        i = 0
        for i in range(num_vertices):
            temp_theta = r.randint(math.pi * 2)
            self.thetas.append(temp_theta)
            temp_dist = (r.randint(5) + 15) * size
            self.dists.append(temp_dist)
        
        self.vertices = self._calc_vertices(position, size, self.num_vertices, self.dists, self.theta)
        g_scale_color = r.randint(128) + 127
        self.color = (g_scale_color, g_scale_color, g_scale_color)

    def _calc_vertices(self, pos, size, num_vertices, dists, thetas):
        vertices = []
        i = 0
        for i in range(num_vertices):
            temp_dist = dists[i]
            temp_theta = thetas[i]
            vertex = (pos[0] + temp_dist * math.cos(temp_theta), pos[1] + temp_dist * math.sin(temp_theta))
            vertices.append(vertex)
        return vertices

    def draw(self, screen)
        self.update()
        self.vertices = self._calc_vertices(self.position, self.size, self.num_vertices, self.dists, self.thetas)
        pg.draw.polygon(screen, self.color, self.vertices, 0)        
