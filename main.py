import pygame as pg
import random as rnd
import math
import time
import sys

from const import Const as c
from player import Player
from bullet import Bullet

# 충돌 감지 함수
def collision(obj1, obj2):
    if math.sqrt((obj1.pos[0] - obj2.pos[0])**2 +
                 (obj1.pos[1] - obj2.pos[1])**2) < 20 :
        return True
    return False

# 텍스트 렌더링 함수
def draw_text(txt, size, pos, color):
    font = pg.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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

bullets = [Bullet(0, rnd.random()*c.size['SCREEN_HEIGHT'], rnd.random()-0.5, rnd.random()-0.5) for _ in range(10)]
time_for_adding_bullets = 0

bg_image = pg.image.load('resource/img/bg.jpg')
bg_pos = 0

pg.mixer.music.load('resource/sounds/bgm.wav')
pg.mixer.music.play(-1)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Game Loop
running = True
gameover = False
getting_event = True
start_time = time.time()
while running:
    dt = clock.tick(FPS)

    bg_pos -= 0.01 * dt
    screen.blit(bg_image, (bg_pos, 0))

    if getting_event :
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
    screen.blit(bg_image, (bg_pos, 0))
    # 플레이어 렌더링
    player.update(FPS)
    player.draw(screen)
    # 총알 렌더링
    for b in bullets:
        b.update_and_draw(dt, screen)
    # 텍스트 렌더링
    if gameover:
        draw_text("GAME OVER", 100, (WIDTH/2-300, HEIGHT/2-50), c.color['RED'])
        txt = "Time: {:.1f} Bullets: {}".format(score, len(bullets))
        draw_text(txt, 32, (WIDTH/2-150, HEIGHT/2 + 50), c.color['WHITE'])

    else:
        score = time.time() - start_time
        txt = "Time: {:.1f}, Bullets: {}".format(score, len(bullets))
        draw_text(txt, 32, (10, 10), c.color['WHITE'])        

    pg.display.update()

    if not gameover:
        # 충돌 감지
        for b in bullets:
            if collision(player, b):
                gameover = True
                getting_event = False
                pg.mixer.music.load('resource/sounds/boom.wav')
                pg.mixer.music.play(1)
                
        # 1초당 총알 하나씩 추가
        time_for_adding_bullets += dt * c.DIFFICULTY
        if time_for_adding_bullets > 1000 :
            bullets.append(Bullet(0, rnd.random()*c.size['SCREEN_HEIGHT'], rnd.random()-0.5, rnd.random()-0.5))
            time_for_adding_bullets -= 1000