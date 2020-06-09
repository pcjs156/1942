import pygame as pg

from const import Const as c
from player import Player

class Background:
    def __init__(self):
        self.image = pg.image.load('resource/img/bg.jpg')
        # 배경화면 이미지를 2배로 키운다. 줌 인 하는 느낌으로?
        self.image = pg.transform.scale(self.image, (c.size['SCREEN_WIDTH']*2, c.size['SCREEN_HEIGHT']*2))
        self.pos = [0, 0]
        self.to = [0, 0]
    
    def draw(self, screen):
        screen.blit(self.image, self.pos)

    # 플레이어와 반대 방향으로 움직이도록 조정한다.
    # main에서 vector를 서로 뒤집을 수도 있지만,,
    def goto(self, x, y):
        self.to[0] -= x
        self.to[1] -= y
    
    def update(self):
        # 배경의 이동 속도를 플레이어의 이동속도의 20%로 고정했다
        self.pos[0] += Player.SPEED/5 * self.to[0]
        self.pos[1] += Player.SPEED/5 * self.to[1]

        # 배경이 화면 밖으로 빠져 나가지 못하도록 설정했다.
        # 화면의 위치(pos)가 처음에 [0,0]이므로 아래와 같이 설정한다.
        self.pos[0] = max(min(self.pos[0], 0), -c.size['SCREEN_WIDTH'])
        self.pos[1] = max(min(self.pos[1], 0), -c.size['SCREEN_HEIGHT'])