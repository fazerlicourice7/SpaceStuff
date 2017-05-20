import pygame as pg
from spaceBodies import CelestialBody
from operator import itemgetter
import math, random as r

class Asteroid(CelestialBody):

    MASS = 1000 # adjust depending on size

    def __init__(self, position = None, size = None, velocity = None, acceleration = None, theta = None, mass = None):
        super(Asteroid, self).__init__(position = position, size = size, velocity = velocity, acceleration = acceleration, theta = theta, mass = self.MASS * size)
        self.num_vertices = r.randint(0, 10) + 10
        self.vertices_info = []
        i = 0
        for i in range(self.num_vertices):
            vertex = {"theta": 0, "dist": 0}
            vertex["theta"] = r.uniform(0, math.pi * 2)
            vertex["dist"] = r.randint(15, 20) * size
            self.vertices_info.append(vertex)

        self.vertices_info = sorted(self.vertices_info, key=itemgetter("theta")) 
        
        self.vertices = self._calc_vertices(position, size, self.vertices_info)
        g_scale_color = r.randint(128, 255)
        self.color = (g_scale_color, g_scale_color, g_scale_color)

    def _calc_vertices(self, pos, size, vertices_info):
        vertices = []
        i = 0
        for i in range(len(vertices_info)):
            temp_dist = vertices_info[i]["dist"]
            temp_theta = vertices_info[i]["theta"]
            vertex = (pos[0] + temp_dist * math.cos(temp_theta), pos[1] + temp_dist * math.sin(temp_theta))
            vertices.append(vertex)
        return vertices

    def _update(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
    
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
    def draw(self, screen):
        self._update()
        self.vertices = self._calc_vertices(self.position, self.size, self.vertices_info)
        pg.draw.polygon(screen, self.color, self.vertices, 0)        
