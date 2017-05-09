import pygame as pg #pygame is a free and open source external library for game development in python
 
class CelestialBody(object):

    def __init__(self, position = None, size = None, velocity = None, acceleration = None, theta = None, mass = None):
        self.position = position if position != None else [0,0]
        self.size = size if size != None else [0,0]
        self.velocity = velocity if velocity != None else [0,0]
        self.acceleration = acceleration if acceleration != None else [0,0]
        self.theta = theta if theta != None else 0 # angle in radians
        self.mass = mass if mass != None else 0

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def get_mass(self):
        return self.mass

    def set_mass(self, mass):
        self.mass = mass

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, xVel, yVel):
        self.velocity = [xVel, yVel]

    def get_acceleration(self):
        return self.acceleration

    def set_acceleration(self, xA, yA):
        self.acceleration = [xA, yA]

    def get_angle(self):
        return self.theta

    def set_angle(self, theta):
        self.theta = theta

    def draw(screen):
        return None
