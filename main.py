import pygame as pg

from const import Const as c
from player import Player

# Pygame Initializing / Setting
pg.init()
WIDTH, HEIGHT = c.size['SCREEN_SIZE']
pg.display.set_caption("총알 피하기")
screen = pg.display.set_mode(c.size['SCREEN_SIZE'])

# FPS Setting
clock = pg.time.Clock()
FPS = c.FPS

# Elements Initializing
player = Player()

# Game Loop
running = True
while running:
    dt = clock.tick(FPS)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    """
    이하 렌더링 : 배경이 맨 위로 와야 됨
    """
    # 배경 렌더링
    screen.fill(c.color['black'])
    # 플레이어 렌더링
    player.draw(screen)

    pg.display.update()