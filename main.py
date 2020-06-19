import pygame as pg
import random as rnd
import time
import sys

from const import Const as c
from player import Player
from bullet import *
from background import Background

from tools import RankingProcessor, draw_text, get_token


# 이상 모듈/클래스 import
# ###################################################################
# 이하 pygame 초기화 / 기본 세팅

pg.init()
WIDTH, HEIGHT = c.size['SCREEN_SIZE']
pg.display.set_caption("총알 피하기")
screen = pg.display.set_mode(c.size['SCREEN_SIZE'])

# FPS Setting
clock = pg.time.Clock()
FPS = c.FPS

# 효과음 로딩
boom_sound = pg.mixer.Sound('resource/sounds/boom.wav')

# 이상 pygame 초기화 / 기본 세팅
# ###################################################################
# 이하 게임 작동 루프
# 게임을 시작하기 위한 초기화 과정과 실제 게임 루프를 묶음으로써
# 특정 입력을 받았을 때 게임을 다시 시작할 수 있도록 함
# 즉, 카운트다운을 포함한 모든 과정
while True:
    # 객체 초기화
    # 플레이어 객체 준비
    player = Player(WIDTH/2 - c.size['PLAYER_WIDTH']/2, HEIGHT/2 - c.size['PLAYER_HEIGHT']/2) # 화면의 중앙쯤 오게 설정

    # 배터리(체럭) 이미지 준비
    battery_image = pg.image.load("resource/img/battery.png")
    battery_image = pg.transform.scale(battery_image, (130, 80))
    battery_image = pg.transform.rotate(battery_image, 90)
    # 배터리에 대한 정보가 담긴 리스트
    battery_cells_info = [((25, i*19+75, 30, 19), c.color["BATTERY"][i]) for i in range(5)]

    # 총알 객체 준비 : 10개의 총알을 랜덤하게 받아옴
    bullets = [Bullet.return_random_bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5) for _ in range(Bullet.initial_bullet_cnt)]
    time_for_adding_bullets = 0

    # 배경 객체 준비(플레이어와 마찬가지로 입력에 의해 움직이도록 하기 위해)
    background = Background()

    # 배경음악 준비
    pg.mixer.music.load('resource/sounds/bgm.wav')
    pg.mixer.music.play(-1)

    # 랭킹 정보 인스턴스 : ranking은 파일의 이름
    ranking_processor = RankingProcessor("ranking")


    # 이상 준비 끝
    # ###################################################################
    # 이하 카운트다운 렌더링 시작


    # 기준 시각으로부터 경과한 시간을 기준으로 3초동안 렌더링을 반복한다
    ready_time = time.time()
    while time.time() - ready_time < 3 :
        # 화면에 표시될 정수형의 초(이 경우 0, 1, 2)
        gap = int(time.time() - ready_time)
        # 화면을 검게 칠한다음
        screen.fill(c.color['BLACK'])
        # 그 위에 3초동안의 카운트다운을 렌더링
        draw_text(screen, "Get Ready!", 80, (330, 250), c.color['RED'])
        draw_text(screen, "{}".format(3 - gap), 50, (495, 400), c.color['WHITE'])
        pg.display.update()
    
    # 새로운 기준 시각으로부터 경과한 시간을 기준으로 1초동안 렌더링을 반복한다
    ready_time = time.time()
    while time.time() - ready_time < 1 :
        screen.fill(c.color['BLACK'])
        draw_text(screen, "Dodge!", 80, (390, 320), c.color['RED'])
        pg.display.update()


    # 이상 게임 시작 전 카운트다운
    # ###################################################################
    # 이하 게임 제어 플래그


    # 카운트다운을 제외한 나머지 부분, 즉 실제 게임 구동 루프 제어
    running = True
    # 중간에 게임이 끝났는지 확인하여 점수판을 렌더링 하고
    # 플레이어가 움직이지 않도록 하며, 충돌 처리도 멈추도록 함
    gameover = False
    # 게임이 끝났을 때 다시 게임을 시작할지 검사하는 역할
    restart = False
    # 해당 코드쪽에서 설명(점수를 한 번만 기록하도록 제어)
    recorded = False


    # 이상 게임 제어 플래그
    # ###################################################################
    # 이하 실제 게임 루프


    # 생존 시간 기록용
    start_time = time.time()
    # 생존시간이 같은 플레이 기록을 서로 구별하기 위해 발급
    token = get_token()
    while running:
        # FPS 설정(
        dt = clock.tick(FPS)

        # ###################################################################
        # 이하 이벤트 리스닝

        # 게임이 종료되면 pg.KEYDOWN, pg.KEYUP 이벤트는 받지 않도록 함
        if not gameover :
            # 이벤트 리스너
            for event in pg.event.get():
                # 종료
                if event.type == pg.QUIT:
                    running = False
                # 키다운
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        player.goto(*c.vector['LEFT'])
                        background.goto(*c.vector['LEFT'])
                    elif event.key == pg.K_RIGHT:
                        player.goto(*c.vector['RIGHT'])
                        background.goto(*c.vector['RIGHT'])
                    elif event.key == pg.K_UP:
                        player.goto(*c.vector['UP'])
                        background.goto(*c.vector['UP'])
                    elif event.key == pg.K_DOWN:
                        player.goto(*c.vector['DOWN'])
                        background.goto(*c.vector['DOWN'])
                # 키업(방향을 다시 반대쪽으로 움직여 to를 [0, 0]으로)
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT:
                        player.goto(*c.vector['RIGHT'])
                        background.goto(*c.vector['RIGHT'])
                    elif event.key == pg.K_RIGHT:
                        player.goto(*c.vector['LEFT'])
                        background.goto(*c.vector['LEFT'])
                    elif event.key == pg.K_UP:
                        player.goto(*c.vector['DOWN'])
                        background.goto(*c.vector['DOWN'])
                    elif event.key == pg.K_DOWN:
                        player.goto(*c.vector['UP'])
                        background.goto(*c.vector['UP'])

        # 게임이 종료되면 게임 종료, 다시시작 이벤트만 받도록 함
        else :
            for event in pg.event.get():
                # 종료
                if event.type == pg.QUIT:
                    running = False
                
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        ranking_processor.render_ranking_board(screen, score)
                        restart = True
                        running = False
                
                    if event.key == pg.K_x:
                        restart = False
                        running = False
                        break

            # 게임이 끝났으므로 화면, 플레이어 모두 움직이지 않도록 설정
            # 키다운만 된 상태로 게임이 종료되면 계속 키다운된 방향으로 이동함
            player.goto(0, 0); player.update(dt);
            background.goto(0, 0); player.update(dt)


        # 이상 이벤트 리스닝
        # ###################################################################
        # 이하 렌더링
        # 텍스트 렌더링 : 위쪽 이벤트 리스닝과 같은 플래그로 제어되지만 기능 분리를 위해 따로 씀


        # 배경 렌더링
        background.update()
        background.draw(screen)

        # 플레이어 렌더링
        player.update(FPS)
        player.draw(screen)

        # 총알 렌더링
        for b in bullets:
            b.update_and_draw(dt, screen)

        # 텍스트 렌더링
        # 게임이 끝났을 경우
        if gameover:
            # ranking 양식에 맞추기 위해 소숫점아래 2번째 자리에서 반올림
            score = round(score, 1)
            # 화면에 표시될 텍스트
            txt = "Time: {:.1f} Bullets: {}".format(score, len(bullets))
            redo_txt = "Press Spacebar to Play Again"
            exit_txt = "Press X to Exit game"

            # 텍스트 렌더링
            draw_text(screen, "GAME OVER", 100, (WIDTH/2-300, 100), c.color['RED'])
            draw_text(screen, txt, 32, (WIDTH/2-150, 200), c.color['WHITE'])
            draw_text(screen, redo_txt, 20, (WIDTH/2-130, 620), c.color['WHITE'])
            draw_text(screen, exit_txt, 20, (WIDTH/2-85, 640), c.color['WHITE'])
            
            # 화면으로 게임이 끝난 것을 파악하는게 이벤트 처리보다 더 직관적이라고 생각해서 이쪽에 씀
            # 이전에 점수를 기록하지 않았을 경우에만 새로 점수를 기록함
            # 이렇게 하지 않으면 게임이 뒷쪽?에서 계속 실행되고 있기 때문에
            # while 루프가 한 번 돌 때마다 이번 판의 기록을 계속 추가함
            if recorded is False:
                recorded = True
                ranking_processor.add_to_ranking_file(score, token)
            # 랭킹 정보 렌더링
            ranking_processor.render_ranking_board(screen, token)


        # 게임이 아직 안 끝났을 경우
        else:
            # 경과 시간 렌더링
            score = time.time() - start_time
            txt = "Time: {:.1f}, Bullets: {}".format(score, len(bullets))
            # 현재 남은 체력 n/5 렌더링
            hp_text = "HP: {}".format(player.HP)
            draw_text(screen, txt, 32, (10, 10), c.color['WHITE'])
            draw_text(screen, hp_text, 20, (20, 180), c.color['RED'])

            # HP바(배터리 렌더링)
            # : 플레이어의 체력에 따라 battery_cells_info에 저장되어 있는 정보에 맞춰 배터리 칸을 렌더링
            screen.blit(battery_image, (0, 50))
            for i in range(player.HP):
                pg.draw.rect(screen, battery_cells_info[5-i-1][1], battery_cells_info[5-i-1][0])

        # 렌더링 요소 업데이트
        pg.display.update()


        # 이상 렌더링
        # ###################################################################
        # 이하 충돌 감지 / 총알 추가 : 렌더링과 같은 플래그로 제어되지만 기능 분리를 위해 따로 씀

        
        # 게임오버되지 않았다면
        if not gameover:
            # 무적시간이 끝났는지 검사하고, 처리한다
            player.invincible_time_chk()

            # 총알 각각에 대한 충돌 검사
            for b in bullets:
                # 만약 충돌했는데 무적 상태가 아니라면
                if player.collision(b) and not player.is_invincible:
                    # 일단 한 대 맞고
                    player.attacked(b)
                    # 만약 맞았는데 체력이 0 이하이면
                    if player.HP <= 0 :
                        # 게임 오버 플래그로 표시하고
                        gameover = True
                        # 꽝! 하는 소리를 한 번 재생한다
                        pg.mixer.Sound.play(boom_sound)
                        # pg.mixer.music.play(1)

            # 1초당 총알 하나씩 추가
            time_for_adding_bullets += dt * Bullet.new_bullet
            if time_for_adding_bullets > 1000 :
                bullets.append(Bullet.return_random_bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))
                time_for_adding_bullets -= 1000

    # 위에서 게임이 종료되었을 때 X를 눌러 게임을 다시 시작하지 않을 경우
    if not restart:
        print('''
88                                     88                                  
88                                     88
88                                     88
88,dPPYba,  8b       d8  ,adPPYba,     88,dPPYba,  8b       d8  ,adPPYba,  
88P'    "8a `8b     d8' a8P_____88     88P'    "8a `8b     d8' a8P_____88
88       d8  `8b   d8'  8PP"""""""     88       d8  `8b   d8'  8PP"""""""  
88b,   ,a8"   `8b,d8'   "8b,   ,aa     88b,   ,a8"   `8b,d8'   "8b,   ,aa  
8Y"Ybbd8"'      Y88'     `"Ybbd8"'     8Y"Ybbd8"'      Y88'     `"Ybbd8"'  
                d8'                                    d8'
               d8'                                    d8'
        ''')
        print("Made by : Yubin Park [ https://github.com/pcjs156 ]")
        sys.exit()