import pygame
from pygame import *
from sys import exit
from random import randint
from math import sin, cos, acos, sqrt, pi

SIZE  = W, H = (400, 600)
NAME  = "WATER"
FPS   = 30
WHITE = (255, 255, 255)
BLACK = (0  , 0  , 0  )
GREY  = (51 , 51 , 51 )
CYAN  = (0  , 255, 255)

QUAN = 70
RAD = 10

def trans_to_degree(rad):
    return rad * 180 / pi

def dist(x0, y0, x1 = 0, y1 = 0):
    return sqrt((x1 - x0)**2 + (y1 - y0)**2)

def rotate(x, y, a, off_x = 0, off_y = 0):
    rx = x * cos(a) - y * sin(a) + off_x
    ry = x * sin(a) + y * cos(a) + off_y
    return [rx, ry]

def angle_v2(x0, y0, x1, y1):
    scl_ml = x0 * x1 + y0 * y1
    a_ = dist(x0, y0)
    b_ = dist(x1, y1)
    if a_ * b_ != 0: cos_a = scl_ml / (a_ * b_)
    else: cos_a = 1
    return acos(cos_a)
    
    

class vect:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def rotate(self, angle):
        self.x = self.x * cos(angle) - self.y * sin(angle)
        self.y = self.y * sin(angle) + self.y * cos(angle)

    def get(self):
        return (self.x, self.y)

    def get_r(self):
        return (round(self.x), round(self.y))

    def rand(self):
        angle = random() * 2*pi
        self.x, self.y = rotate(0, -SPEED, angle)

    def add(self, sec):
        self.x = self.x + sec.x
        self.y = self.y + sec.y

    def subst(self, sec):
        return vect(self.x - sec.x, self.y - sec.y)
        
    def mult(self, scl):
        self.x = self.x * scl
        self.y = self.y * scl

    def get_mult(self, scl):
        return vect(self.x * scl, self.y * scl)

    def sum(self, sec, scl = 1):
        return vect(self.x + sec.x * scl, self.y + sec.y * scl)

    def leng(self):
        return sqrt(self.x**2 + self.y**2)

GRAV = vect(0, 1)
DIAG = dist(W, H)

class Drop:
    def __init__(self, x, y):
        self.pos = vect(x, y)
        self.vel = vect(randint(-4, 4), 0)
        self.acc = vect()
        self.r = RAD

    def collide(self, sec):
        d = dist(self.pos.x, self.pos.y, sec.pos.x, sec.pos.y)

        if d <= self.r + sec.r:
            vect = self.pos.subst(sec.pos)
            lost = (self.r + sec.r - d)/(self.r + sec.r)
            self.pos.add(vect.get_mult(lost))
            if self.pos.x >= sec.pos.x:
                vect.mult(-1)
                
            angle = angle_v2(self.vel.x, self.vel.y, vect.x, vect.y)
            
            if self.pos.y >= sec.pos.y:
                angle = angle * -1
                
            self.vel.rotate(2*angle)
            self.vel.mult(-1)
            added = sec.vel
            added.mult(0.75)
            self.vel.add(added) 
            
    def applyForce(self, force):
        self.acc.add(force)

    def update(self, drops):
        for el in drops:
            if el != self:
                self.collide(el)
        if self.pos.y != H - self.r or self.vel.y < 0:        
            self.applyForce(GRAV)
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
        self.vel.mult(0.965)

        if self.pos.y > H - self.r:
            self.pos.y = H - self.r
            self.vel.y = self.vel.y * (-1)
        if self.pos.x < self.r:
            self.pos.x = self.r
            self.vel.x = self.vel.x * (-1)
        if self.pos.x > W - self.r:
            self.pos.x = W - self.r
            self.vel.x = self.vel.x * (-1)

        

    def draw(self, screen):
        draw.circle(screen, CYAN, self.pos.get_r(), self.r)

def run():
    pygame.init()
    display.set_caption(NAME)
    screen = display.set_mode(SIZE)
    clock = time.Clock()

    drops = []
    #drops.append(Drop(30, 50))
    #drops.append(Drop(150, 50))
    #drops.append(Drop(400, 50))

    for n in range(QUAN):
        drops.append(Drop(randint(0, W), randint(0, H)))

    while 1:
        clock.tick(FPS)
        screen.fill(GREY)

        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()

        for el in drops:
            el.update(drops)
            el.draw(screen)

        display.update()




if __name__ == "__main__":
    run()
