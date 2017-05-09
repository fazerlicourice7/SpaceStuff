import pygame as pg #pygame is a free and open source external library for game development in python
from spaceBodies import CelestialBody
import math

class Spaceship(CelestialBody):

    MAX_VELOCITY = 2  # pixel / frame
    COEFF_FRICTION = .009
    RATE_OF_ROT = math.pi/128


    def __init__(self, position = None, size = None, velocity = None, acceleration = None, theta = None, mass = None):
        super(Spaceship, self).__init__(position = position, size = size, velocity = velocity, acceleration = acceleration, theta = theta, mass = mass)
        self.health = 3
        self.update()
    
    def rotate(self, direction):
        self.theta += (direction)*(self.RATE_OF_ROT)

    def get_vertices(self):
        return self.vertices

    def set_velocity(self, xVel, yVel): # used only for initialization (0,0)
        self.velocity = [xVel, -1*yVel]

    def set_acceleration(self, xA, yA):
        self.acceleration = [xA, yA]

    def get_acceleration(self):
        return self.acceleration

    def set_health(self, health):
        self.health = health

    def update_health(self, dHealth):
        self.health += dHealth

    def get_health(self):
        return self.health

    def calc_vertices(self):
        vertexA = (self.position[0] + int(40*math.cos(self.theta)), self.position[1] - int(40*math.sin(self.theta)))
        vertexB = (self.position[0] + int(20*math.cos(self.theta +(5*(math.pi))/6)), self.position[1] - int(20*math.sin(self.theta + (5*(math.pi))/6)))
        vertexC = (self.position[0] + int(20*math.cos(self.theta +(7*(math.pi))/6)), self.position[1] - int(20*math.sin(self.theta + (7*(math.pi))/6)))

        self.vertices = [vertexA, vertexB, self.position, vertexC]

    def update(self):
        if self.theta >= 2*math.pi:
            self.theta -= 2*math.pi
        elif self.theta <= -2*math.pi:
            self.theta += 2*math.pi

        friction = [self.COEFF_FRICTION * -self.velocity[0], self.COEFF_FRICTION * -self.velocity[1]]
        self.acceleration[0] += friction[0]
        self.acceleration[1] += friction[1]
        
        if (math.sqrt(math.pow(self.velocity[0], 2) + math.pow(self.velocity[1], 2)) < self.MAX_VELOCITY):
            self.velocity[0] += self.acceleration[0]
            self.velocity[1] += self.acceleration[1]
    
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def draw(self, screen, color, width = 0):
        self.update()
        self.calc_vertices()
        pg.draw.polygon(screen, color, self.vertices, width)
