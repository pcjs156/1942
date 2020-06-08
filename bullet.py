import pygame as pg

import random as rnd

from const import Const as c

class Bullet:
    bullet_cnt = 10
    def __init__(self, x, y, to_x, to_y):
        self.pos = [x, y]
        self.to = [to_x, to_y]
        self.radius = c.size['BULLET_RADIUS']
        self.color = c.color['RED']
    
    def update_and_draw(self, dt, screen):
        self.pos[0] = (self.pos[0] + dt*self.to[0]) % c.size['SCREEN_WIDTH']
        self.pos[1] = (self.pos[1] + dt*self.to[1]) % c.size['SCREEN_HEIGHT']

        pos_int = (int(self.pos[0]), int(self.pos[1]))
        pg.draw.circle(screen, self.color, pos_int, self.radius)