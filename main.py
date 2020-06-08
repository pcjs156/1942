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
player = Player(WIDTH/2-c.size['PLAYER_WIDTH']/2, HEIGHT/2-c.size['PLAYER_HEIGHT']/2) # 화면의 중앙쯤 오게 설정

# Game Loop
running = True
while running:
    dt = clock.tick(FPS)
    
    # 이벤트 리스너
    for event in pg.event.get():
        # 종료
        if event.type == pg.QUIT:
            running = False
        # 키다운
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player.goto(*c.vector['LEFT'])
            elif event.key == pg.K_RIGHT:
                player.goto(*c.vector['RIGHT'])
            elif event.key == pg.K_UP:
                player.goto(*c.vector['UP'])
            elif event.key == pg.K_DOWN:
                player.goto(*c.vector['DOWN'])
            elif event.key == pg.K_left:
                player.goto(*c.vector['DOWN'])
            elif event.key == pg.K_DOWN:
                player.goto(*c.vector['DOWN'])
        # 키업(방향을 다시 반대쪽으로 움직여 to를 [0, 0]으로)
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                player.goto(*c.vector['RIGHT'])
            elif event.key == pg.K_RIGHT:
                player.goto(*c.vector['LEFT'])
            elif event.key == pg.K_UP:
                player.goto(*c.vector['DOWN'])
            elif event.key == pg.K_DOWN:
                player.goto(*c.vector['UP'])

    """
    이하 렌더링 : 배경이 맨 위로 와야 됨
    """
    # 배경 렌더링
    screen.fill(c.color['black'])
    # 플레이어 렌더링
    player.update(FPS)
    player.draw(screen)

    pg.display.update()