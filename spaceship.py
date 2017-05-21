import pygame as pg #pygame is a free and open source external library for game development in python
from spaceBodies import CelestialBody
import math

class Spaceship(CelestialBody):

    MAX_VELOCITY = 2  # pixel / frame
    COEFF_FRICTION = .009
    RATE_OF_ROT = math.pi/128
    AMMO = 10
    FUEL = 20
    HEALTH = 5
    red = (255, 0, 0)
    blue = (0, 0, 255)
    
    def __init__(self, position = None, size = None, velocity = None, acceleration = None, theta = None, mass = None):
        super(Spaceship, self).__init__(position = position, size = size, velocity = velocity, acceleration = acceleration, theta = theta, mass = mass)
        self.health = self.HEALTH
        self.ammo = self.AMMO
        self.fuel = self.FUEL
        self.update()
        self.calc_vertices()
    
    def rotate(self, direction):
        self.theta += (direction)*(self.RATE_OF_ROT)

    def get_vertices(self):
        return self.vertices

    def set_velocity(self, xVel, yVel): # used only for initialization (0,0)
        self.velocity = [xVel, -1*yVel]

    def set_health(self, health):
        self.health = health

    def update_health(self, dHealth):
        self.health += dHealth

    def get_health(self):
        return self.health

    def get_ammo(self):
        return self.ammo

    def update_ammo(self, dAmmo):
        self.ammo += dAmmo

    def get_fuel(self):
        return self.fuel

    def update_fuel(self, dFuel):
        self.fuel += dFuel

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

    def draw_stats(self, screen, location, color, multiplier = 1):
        i = 0
        health_radius = 10
        x = location[0] + multiplier * health_radius * 2
        y = location[1] + health_radius * 2
        for i in range(self.health):
            pg.draw.circle(screen, self.red, (x, y), health_radius, 0)
            x += multiplier * health_radius * 3
        y += health_radius * 3
        x = location[0] + multiplier * health_radius * 2
        i = 0
        for i in range(self.ammo):
            rect = pg.Rect(x, y, health_radius / 2, health_radius)
            pg.draw.rect(screen, color, rect, 0)
            x += multiplier * health_radius * 2
        y += health_radius * 3
        x = location[0] + multiplier * health_radius
        i = 0

        fuel_rect = pg.Rect(x, y, self.fuel * health_radius, health_radius)
        if(multiplier == -1):
            fuel_rect = pg.Rect(x + multiplier * self.fuel * health_radius, y, self.fuel * health_radius, health_radius)
            
        pg.draw.rect(screen, self.blue, fuel_rect, 0)
            
        
