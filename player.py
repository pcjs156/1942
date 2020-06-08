import pygame as pg

from const import Const as c

class Player:
    def __init__(self):
        self.image = pg.image.load('resource/img/player.png')
        self.image = pg.transform.scale(self.image, c.size['PLAYER_SIZE'])
        self.pos = [0, 0]
    
    def draw(self, screen):
        screen.blit(self.image, self.pos)
