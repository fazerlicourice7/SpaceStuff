import pygame as pg #pygame is a free and open source external library for game development in python

from asteroid import Asteroid
from display import Display
from spaceship import Spaceship
from projectile import Projectile
from planets import Planet

import math
from random import randint, uniform
import os, sys

pg.init()
pg.font.init()

screen = Display()
screen = screen.get_screen()

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

THRUST_ACCEL = .0125 # pixel / frame^2


def __init_planet__():
    r = randint(30, 150)
    m = randint(3 * 10**5, 3 * 10**6)
    x = randint(int((1/3) * screen.get_width()), int((2/3) * screen.get_width()))
    #y = randint(int(screen.get_height() / 4), int(3 * screen.get_height() / 4))
    #x = randint(0, screen.get_width())
    y = randint(int(screen.get_height() / 4), screen.get_height())
    pos = [x, y]
    return Planet(position = pos, mass = m, radius = r)

def __init_asteroid__():
    size = randint(1,3)
    x = randint(0, screen.get_width())
    y = randint(0, screen.get_height())
    Vx = uniform(0,1.5)
    Vy = uniform(0,1.5)
    return Asteroid(position = [x,y], size = size, velocity = [Vx, Vy])

def __init_1__():
    pos = [screen.get_width() / 6, screen.get_height() / 2]
    v = [0, 0]
    angle = 0
    return Spaceship(position = pos, velocity = v, theta = angle)

def __init_2__():
    pos = [5 * screen.get_width() / 6, screen.get_height() / 2]
    v = [0, 0]
    angle = math.pi
    return Spaceship(position = pos, velocity = v, theta = angle)

def touching_edge(obj, screen):
    if(obj.get_position()[0] <= 0 and obj.get_velocity()[0] < 0):
        return 1
    elif(obj.get_position()[0] >= screen.get_width() and obj.get_velocity()[0] > 0):
        return 2
    elif(obj.get_position()[1] <= 0 and obj.get_velocity()[1] < 0):
        return 3
    elif(obj.get_position()[1] >= screen.get_height() and obj.get_velocity()[1] > 0):
        return 4
    else:
        return -1

def cleanup_projectiles(projectiles, ship, screen):
    for p in projectiles:
        if touching_edge(p, screen) != -1:
            projectiles.remove(p)
            ship.update_ammo(1)

    return projectiles

def split_up_asteroid(asteroid): # size3 -> 2 size2; size2 -> 3 size1
    a_p = asteroid.get_position()
    a_v = asteroid.get_velocity()
    a_m = asteroid.get_mass()
    if(asteroid.size == 1):
        return None
    elif(asteroid.size == 2):
        asteroids3 = []
        i = 0
        for i in range(3):
            if i == 2:
                p0 = [i * asteroids3[0].get_mass() for i in asteroids3[0].get_velocity()]
                p1 = [i * asteroids3[0].get_mass() for i in asteroids3[1].get_velocity()]
                px = (a_v[0] * a_m) - (p0[0] + p1[0])
                py = (a_v[1] * a_m) - (p0[1] + p1[1])
                vel = [px / (a_m / 2), py / (a_m / 2)]
                theta = math.atan(vel[1] / vel[0])
            else:
                p = uniform(math.hypot(a_m * a_v[0], a_m * a_v[1]) * 1 / 10, math.hypot(a_m * a_v[0], a_m * a_v[1]) * 4 / 10)
                theta = uniform(0, 2 * math.pi)
                velX = p * math.cos(theta) / (a_m / 2)
                velY = p * math.sin(theta) / (a_m / 2)
                vel = [velX, velY]
            pos = [a_p[0] + math.cos(theta) * 10, a_p[1] + math.sin(theta) * 10]  #asteroid gets moved slightly outward in direction of velocity
            a = Asteroid(position = pos, size = 1, velocity = vel)
            asteroids3.append(a)
        return asteroids3
    elif(asteroid.size == 3):
        asteroids2 = []
        i = 0
        for i in range(2):
            if i == 1:
                p0 = [i * asteroids2[0].get_mass() for i in asteroids2[0].get_velocity()]
                px = (a_v[0] * a_m) - p0[0]
                py = (a_v[1] * a_m) - p0[1]
                vel = [px / (a_m * 2 / 3), py / (a_m * 2 / 3)]
                theta = math.atan(vel[1] / vel[0])
            else:
                p = uniform(math.hypot(a_m * a_v[0], a_m * a_v[1]) * 1 / 4, math.hypot(a_m * a_v[0], a_m * a_v[1]) * 3 / 4)
                theta = uniform(0, 2 * math.pi)
                velX = p * math.cos(theta) / (a_m * 2 / 3)
                velY = p * math.sin(theta) / (a_m * 2 / 3)
                vel = [velX, velY]
            pos = [a_p[0] + math.cos(theta) * 10, a_p[1] + math.sin(theta) * 10]  #asteroid gets moved slightly outward in direction of velocity
            a = Asteroid(position = pos, size = 2, velocity = vel)
            asteroids2.append(a)
        return asteroids2
    return None

def getXDirectionTowards(shipC, planetP):
    if(shipC.get_position()[0] < planetP.get_position()[0]):
        return 1
    elif(shipC.get_position()[0] > planetP.get_position()[0]):
        return -1
    else:
        return 0

def getYDirectionTowards(shipC, planetP):
    if(shipC.get_position()[1] < planetP.get_position()[1]):
        return 1
    elif(shipC.get_position()[1] > planetP.get_position()[1]):
        return -1
    else:
        return 0

def gravity(object1, object2): #calculates the force and direction on object1.
    G = 6.672867 * math.pow(10, -5)
    xDist = abs(object2.get_position()[0] - object1.get_position()[0])
    yDist = abs(object2.get_position()[1] - object1.get_position()[1])
    g = G * object1.get_mass() * object2.get_mass() / ((xDist ** 2) + (yDist ** 2))
    angle = math.atan(yDist /xDist)
    gX = g * math.cos(angle)
    gY = g * math.sin(angle)
    return [getXDirectionTowards(object1, object2) * gX, getYDirectionTowards(object1, object2) * gY]

def game_over(screen, winner): #if winner = 0 the game is a draw
    red = (255, 0, 0)
    font = pg.font.SysFont("sansserif", 128)
    if(winner == 0):
        gameOver = font.render("GAME OVER!", False, red)
        result = font.render("DRAW", False, red)

    elif(winner == 1):
        gameOver = font.render("GAME OVER!", False, white)
        result = font.render("PLAYER 1 WINS", False, white)
        

    elif(winner == 2):
        gameOver = font.render("GAME OVER!", False, yellow)
        result = font.render("PLAYER 2 WINS", False, yellow)

    go = ((screen.get_width() / 2) - (gameOver.get_width() / 2), (screen.get_height() / 2) - gameOver.get_height())
    r = ((screen.get_width() / 2) - (result.get_width() / 2), (screen.get_height() / 2))
    screen.blit(gameOver, go)
    screen.blit(result, r)
    pg.display.flip()
    
spaceship1 = __init_1__()
projectiles1 = []
characteristics1 = {"thrust": False, "rotate_cw": False, "rotate_ccw": False, "fire": False, "thrust_counter": 0, "recharge_counter": 0}

spaceship2 = __init_2__()
projectiles2 = []
characteristics2 = {"thrust": False, "rotate_cw": False, "rotate_ccw": False, "fire": False, "thrust_counter": 0, "recharge_counter": 0}


planets = []
#for i in range(0, 3):
planets.append(__init_planet__())

asteroids = []
i = 0
for i in range(randint(2,5)):
    asteroids.append(__init_asteroid__())

frame_counter = 0
while 1:
    #GET INPUT
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            pg.quit()
            sys.exit()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_F5:
                os.execl(sys.executable, sys.executable, *sys.argv)
                pg.display.quit()
                pg.quit()
                sys.exit()

            if event.key == pg.K_w:
                characteristics1["thrust"] = True
            elif event.key == pg.K_d:
                characteristics1["rotate_cw"] = True
            elif event.key == pg.K_a:
                characteristics1["rotate_ccw"] = True
            if event.key == pg.K_SPACE:
                characteristics1["fire"] = True

            if event.key == pg.K_UP:
                characteristics2["thrust"] = True
            elif event.key == pg.K_RIGHT:
                characteristics2["rotate_cw"] = True
            elif event.key == pg.K_LEFT:
                characteristics2["rotate_ccw"] = True
            if event.key == pg.K_DOWN:
                characteristics2["fire"] = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                characteristics1["thrust"] = False           
            elif event.key == pg.K_d:
                characteristics1["rotate_cw"] = False
            elif event.key == pg.K_a:
                characteristics1["rotate_ccw"] = False
            if event.key == pg.K_SPACE:
                characteristics1["fire"] = False

            if event.key == pg.K_UP:
                characteristics2["thrust"] = False
            elif event.key == pg.K_RIGHT:
                characteristics2["rotate_cw"] = False
            elif event.key == pg.K_LEFT:
                characteristics2["rotate_ccw"] = False
            if event.key == pg.K_DOWN:
                characteristics2["fire"] = False



    #UPDATE INFORMATION
    accelG1 = [0, 0]
    accelG2 = [0, 0]
    for planet in planets:
        f_g_1 = gravity(spaceship1, planet)
        f_g_2 = gravity(spaceship2, planet)
    
        accelG1[0] += f_g_1[0] / spaceship1.get_mass()
        accelG1[1] += f_g_1[1] / spaceship1.get_mass()
        
        accelG2[0] += f_g_2[0] / spaceship2.get_mass()
        accelG2[1] += f_g_2[1] / spaceship2.get_mass()

        for a in asteroids:
            accelG = [grav / a.get_mass() for grav in gravity(a, planet)]
            a.set_acceleration(accelG[0], accelG[1])

        for p in projectiles1:
            accelG = [grav / p.get_mass() for grav in gravity(p, planet)]
            p.set_acceleration(accelG[0], accelG[1])

        for p in projectiles2:
            accelG = [grav / p.get_mass() for grav in gravity(p, planet)]
            p.set_acceleration(accelG[0], accelG[1])

    #print("ship1 position: " + str(spaceship1.get_position()) +"; accelG: " + str(accelG1) + "; vel: " + str(spaceship1.get_velocity()))
    #print("ship2 position: " + str(spaceship2.get_position()) +"; accelG: " + str(accelG2) + "; vel: " + str(spaceship2.get_velocity()))

    if(characteristics1["thrust"]):
        if(spaceship1.get_fuel() > 0):
            characteristics1["recharge_counter"] = 0
            xA = THRUST_ACCEL * math.cos(spaceship1.get_angle())
            yA = THRUST_ACCEL * -math.sin(spaceship1.get_angle())
            spaceship1.set_acceleration(accelG1[0] + xA, accelG1[1] + yA)
            characteristics1["thrust_counter"] += 1
        elif(spaceship1.get_fuel() == 0):
            characteristics1["thrust"] = False
        if(characteristics1["thrust_counter"] % 60 == 0):
            spaceship1.update_fuel(-1)
    if(characteristics1["rotate_cw"]):
        spaceship1.rotate(-1)
    if(characteristics1["rotate_ccw"]):
        spaceship1.rotate(1)
    if(not characteristics1["thrust"]):
        spaceship1.set_acceleration(accelG1[0], accelG1[1])
        characteristics1["thrust_counter"] = 0
        characteristics1["recharge_counter"] += 1
        if(characteristics1["recharge_counter"] % 60 == 0 and characteristics1["recharge_counter"] >= 240):
            if(spaceship1.get_fuel() < 20):
                spaceship1.update_fuel(1)
    if(characteristics1["fire"]):
        if(frame_counter % 30 == 0):
            if(spaceship1.get_ammo() > 0):
                projectiles1.append(Projectile(list(spaceship1.get_vertices()[0]), [math.cos(spaceship1.get_angle()), math.sin(spaceship1.get_angle())], white))
                spaceship1.update_ammo(-1)
        frame_counter += 1


    if(characteristics2["thrust"]):
        if(spaceship2.get_fuel() > 0):
            characteristics2["recharge_counter"] = 0
            xA = THRUST_ACCEL * math.cos(spaceship2.get_angle())
            yA = THRUST_ACCEL * -math.sin(spaceship2.get_angle())
            spaceship2.set_acceleration(accelG2[0] + xA, accelG2[1] + yA)
            characteristics2["thrust_counter"] += 1
        elif(spaceship2.get_fuel() == 0):
            characteristics2["thrust"] = False
        if(characteristics2["thrust_counter"] % 60 == 0):
            spaceship2.update_fuel(-1)
    if(characteristics2["rotate_cw"]):
        spaceship2.rotate(-1)
    if(characteristics2["rotate_ccw"]):
        spaceship2.rotate(1)
    if(not characteristics2["thrust"]):
        spaceship2.set_acceleration(accelG2[0], accelG2[1])
        characteristics2["thrust_counter"] = 0
        characteristics2["recharge_counter"] += 1
        if(characteristics2["recharge_counter"] % 60 == 0 and characteristics2["recharge_counter"] >= 240):
            if(spaceship2.get_fuel() < 20):
                spaceship2.update_fuel(1)
    if(characteristics2["fire"]):
        if(frame_counter % 30 == 0):
            if(spaceship2.get_ammo() > 0):
                projectiles2.append(Projectile(list(spaceship2.get_vertices()[0]), [math.cos(spaceship2.get_angle()), math.sin(spaceship2.get_angle())], yellow))
                spaceship2.update_ammo(-1)
        frame_counter += 1
   
    projectiles1 = cleanup_projectiles(projectiles1, spaceship1, screen)
    projectiles2 = cleanup_projectiles(projectiles2, spaceship2, screen)

    touch_edge = touching_edge(spaceship1, screen)
    if(touch_edge != -1):
        pos = spaceship1.get_position()
        vel = spaceship1.get_velocity()
        if(touch_edge == 1 or touch_edge == 2):
            spaceship1.set_position([pos[0] + (-1 * vel[0] / math.fabs(vel[0])) * 5 * math.hypot(vel[0], vel[1]), pos[1]])
        elif(touch_edge == 3 or touch_edge == 4):
            spaceship1.set_position([pos[0], pos[1] + (-1 * vel[1] / math.fabs(vel[1])) * 5 * math.hypot(vel[0], vel[1])])
        spaceship1.set_velocity(0, 0)

    touch_edge = touching_edge(spaceship2, screen)
    if(touch_edge != -1):
        pos = spaceship2.get_position()
        vel = spaceship2.get_velocity()
        if(touch_edge == 1 or touch_edge == 2):
            spaceship2.set_position([pos[0] + (-1 * vel[0] / math.fabs(vel[0])) * 5 * math.hypot(vel[0], vel[1]), pos[1]])
        elif(touch_edge == 3 or touch_edge == 4):
            spaceship2.set_position([pos[0], pos[1] + (-1 * vel[1] / math.fabs(vel[1])) * 5 * math.hypot(vel[0], vel[1])])
        spaceship2.set_velocity(0, 0)

    for a in asteroids:
        touch_edge = touching_edge(a, screen)
        if(touch_edge != -1):
            if(touch_edge == 1 or touch_edge == 2):
                vel = a.get_velocity()
                pos = a.get_position()
                a.set_position([pos[0] + (-1 * vel[0] / math.fabs(vel[0])) * 5 * math.hypot(vel[0], vel[1]), pos[1]])
                a.set_velocity(-1 * vel[0], vel[1])
            elif(touch_edge == 3 or touch_edge == 4):
                vel = a.get_velocity()
                pos = a.get_position()
                a.set_position([pos[0], pos[1] + (-1 * vel[1] / math.fabs(vel[1])) * 5 * math.hypot(vel[0], vel[1])])
                a.set_velocity(vel[0], -1 * vel[1])

    for p in projectiles1:
        if(p.hit_obj(spaceship2)): # spaceship-projectile collision
            projectiles1.remove(p)
            spaceship1.update_ammo(1)
            spaceship2.update_health(-1)
            continue #required so that asteroid-projectile collisions not checked if p is already removed from list.
        for a in asteroids: # asteroid-projectile collision
            if(p.hit_obj(a)):
                projectiles1.remove(p)
                spaceship1.update_ammo(1)
                temp_asteroids = split_up_asteroid(a)
                asteroids.remove(a)
                if (temp_asteroids != None):
                    asteroids += temp_asteroids
                break

    for p in projectiles2:
        if(p.hit_obj(spaceship1)): # spaceship-projectile collision
            projectiles2.remove(p)
            spaceship2.update_ammo(1)
            spaceship1.update_health(-1)
            continue #required so that asteroid-projectile collisions not checked if p is already removed from list.
        for a in asteroids: # asteroid-projectile collision
            if(p.hit_obj(a)):
                projectiles2.remove(p)
                spaceship2.update_ammo(1)
                temp_asteroids = split_up_asteroid(a)
                asteroids.remove(a)
                if (temp_asteroids != None):
                    asteroids += temp_asteroids
                break

    for a in asteroids: # Check asteroid-spaceship collision
        if(a.hit_obj(spaceship1)):
            spaceship1.update_health(-1)
            vel = a.get_velocity()
            #a.set_velocity(-1 * vel[0], -1 * vel[1])
            asteroids.remove(a)
        if(a.hit_obj(spaceship2)):
            spaceship2.update_health(-1)
            vel = a.get_velocity()
            #a.set_velocity(-1 * vel[0], -1 * vel[1])
            asteroids.remove(a)

    for planet in planets:
        position = planet.get_position()
        pos1 = spaceship1.get_position()
        pos2 = spaceship2.get_position()
        dist1 = math.hypot(pos1[0] - position[0], pos1[1] - position[1])
        dist2 = math.hypot(pos2[0] - position[0], pos2[1] - position[1])

        if(dist1 <= planet.get_radius()): #planet-spaceship collision
            health = spaceship1.get_health() - 1
            spaceship1 = __init_1__()
            spaceship1.set_health(health)
        if(dist2 <= planet.get_radius()):
            health = spaceship2.get_health() - 1
            spaceship2 = __init_2__()
            spaceship2.set_health(health)

        for p in projectiles1:
            pos = p.get_position()
            dist = math.hypot(pos[0] - position[0], pos[1] - position[1])
            if(dist <= planet.get_radius()): #planet-projectile collision
                projectiles1.remove(p)
                spaceship1.update_ammo(1)

        for p in projectiles2:
            pos = p.get_position()
            dist = math.hypot(pos[0] - position[0], pos[1] - position[1])
            if(dist <= planet.get_radius()): #planet-projectile collision
                projectiles2.remove(p)
                spaceship2.update_ammo(1)

        for a in asteroids:
            for vertex in a.get_vertices():
                dist = math.hypot(vertex[0] - position[0], vertex[1] - position[1])
                if(dist <= planet.get_radius()):
                    temp_asteroids = split_up_asteroid(a)
                    asteroids.remove(a)
                    if (temp_asteroids != None):
                        asteroids += temp_asteroids
                    break

    #UPDATE SCREEN
    screen.fill(black) #black(rgb)  = 0,0,0
    for p in projectiles1:
        p.draw(screen)
    spaceship1.draw(screen, white, width = 3)
    spaceship1.draw_stats(screen, (0,0), white, multiplier = 1)

    for p in projectiles2:
       p.draw(screen)
    spaceship2.draw(screen, yellow, width = 3)
    spaceship2.draw_stats(screen, (screen.get_width(), 0), yellow, multiplier = -1)

    for a in asteroids:
        a.draw(screen)

    for planet in planets:
        planet.draw(screen)
    
    pg.display.flip()

    if(spaceship1.get_health() <= 0 and spaceship2.get_health() <= 0):
        game_over(screen, 0)
        break
    elif(spaceship1.get_health() <= 0):
        game_over(screen, 2)
        break
    elif(spaceship2.get_health() <= 0):
        game_over(screen, 1)
        break

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_F5:
                os.execl(sys.executable, sys.executable, *sys.argv)
                pg.display.quit()
                pg.quit()
                sys.exit()
