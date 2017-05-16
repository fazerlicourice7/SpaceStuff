import pygame as pg #pygame is a free and open source external library for game development in python

from display import Display
from spaceship import Spaceship
from projectile import Projectile
from planets import Planet

import math
from random import randint
import os, sys

pg.init()
pg.font.init()

screen = Display()
screen = screen.get_screen()

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

THRUST_ACCEL = .0125 # pixel / frame^2
SHIP_MASS = 1000


def __init_planet__():
    r = randint(50, 300)
    m = randint(10**6, 10**7)
    x = randint(int((1/3) * screen.get_width()), int((2/3) * screen.get_width()))
    y = randint(0, screen.get_height())
    pos = [x, y]
    planet = Planet(position = pos, mass = m, radius = r)
    return planet

def __init_1__():
    pos = [screen.get_width() / 6, screen.get_height() / 2]
    v = [0, 0]
    angle = 0
    return Spaceship(position = pos, velocity = v, theta = angle, mass = SHIP_MASS)

def __init_2__():
    pos = [5 * screen.get_width() / 6, screen.get_height() / 2]
    v = [0, 0]
    angle = math.pi
    return Spaceship(position = pos, velocity = v, theta = angle, mass = SHIP_MASS)

def touching_edge(spaceship, screen):
    if(spaceship.get_position()[0] <= 0 and spaceship.get_velocity()[0] < 0):
        return True
    elif(spaceship.get_position()[0] >= screen.get_size()[0] and spaceship.get_velocity()[0] > 0):
        return True
    elif(spaceship.get_position()[1] <= 0 and spaceship.get_velocity()[1] < 0):
        return True
    elif(spaceship.get_position()[1] >= screen.get_size()[1] and spaceship.get_velocity()[0] > 0):
        return True
    else:
        return False

def cleanup_projectiles(projectiles, ship, screen):
    for p in projectiles:
        if touching_edge(p, screen):
            projectiles.remove(p)
            ship.update_ammo(1)

    return projectiles

def gravity(object1, object2): #calculates the force and direction on object1.
    G = 6.672867 * math.pow(10, -11)
    xDist = object2.get_position()[0] - object1.get_position()[0]
    yDist = object2.get_position()[1] - object1.get_position()[1]
    gX = G * object1.get_mass() * object2.get_mass() / (xDist ** 2)
    gY = G * object1.get_mass() * object2.get_mass() / (yDist ** 2)
    xDir = xDist / math.fabs(xDist)
    yDir = yDist / math.fabs(yDist)
    return [xDir * gX, yDir * gY]

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

planet = __init_planet__()

frame_counter = 0
while 1:
    #GET INPUT
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            pg.quit()
            sys.exit()

        elif event.type == pg.KEYDOWN:
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
            if event.key == pg.K_RCTRL:
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
            if event.key == pg.K_RCTRL:
                characteristics2["fire"] = False



    #UPDATE INFORMATION


    #f_g_1 = gravity(spaceship1, planet)
    #f_g_2 = gravity(spaceship2, planet)

    #accelG1 = [f_g_1[0] / spaceship1.get_mass(), f_g_1[1] / spaceship1.get_mass()]
    #accelG2 = [f_g_2[0] / spaceship2.get_mass(), f_g_2[1] / spaceship2.get_mass()]
    #accelG1 = f_g_1
    #accelG2 = f_g_2
    accelG1 = [0,0]
    accelG2 = [0,0]

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
    
    if(touching_edge(spaceship1, screen)):
        spaceship1.set_velocity(0, 0)
    if(touching_edge(spaceship2, screen)):
        spaceship2.set_velocity(0, 0)

    for p in projectiles1:
        if(p.hit_ship(spaceship2)):
            projectiles1.remove(p)
            spaceship1.update_ammo(1)
            spaceship2.update_health(-1)

    for p in projectiles2:
        if(p.hit_ship(spaceship1)):
            projectiles2.remove(p)
            spaceship2.update_ammo(1)
            spaceship1.update_health(-1)

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
    
    #planet.draw()
    
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
