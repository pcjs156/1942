import pygame as pg

from const import Const as c

class Player:
    def __init__(self):
        self.image = pg.image.load('resource/img/player.png')
        self.image = pg.transform.scale(self.image, c.size['PLAYER_SIZE'])
        # 좌표는 각각 [x, y]좌표
        self.pos = [0, 0] # 플레이어의 현재 위치(update에 의해 갱신됨)
        self.to = [0, 0] # 플레이어가 이동할 방향(상, 하, 좌, 우, ...)
    
    # 화면에 플레이어를 렌더링
    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def goto(self, x, y):
        self.to[0] += x
        self.to[1] += y

    # 화면상의 플레이어 위치를 업데이트
    def update(self, dt):
        self.pos[0] += dt * self.to[0]
        self.pos[1] += dt * self.to[1]