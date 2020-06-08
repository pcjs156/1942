import pygame as pg

from const import Const as c

# Pygame Initializing / Setting
pg.init()
WIDTH, HEIGHT = c.size['SCREEN_SIZE']
pg.display.set_caption("총알 피하기")
screen = pg.display.set_mode(c.size['SCREEN_SIZE'])

clock = pg.time.Clock()
FPS = c.FPS

# Game Loop
running = True
while running:
    dt = clock.tick(FPS)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(c.color['black'])

    pg.display.update()