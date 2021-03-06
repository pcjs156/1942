# 플레이어(비행기) 클래스

import pygame as pg
import time
import math

from const import Const as c


# 이상 모듈/클래스 import 
# ###################################################################
# 이하 Player 클래스


class Player:
    # ###################################################################
    # 이하 Player 클래스 기본 설정

    # 플레이어 기본 속도
    SPEED = 30
    # 플레이어 무적 시간(초)
    INVINCIBLE = 2

    # 미션 2 수정 : Player 이미지를 폭발 이미지로 바꾸는 코드를 main.py에서 player.py로 옮김 
    boom_image = pg.image.load('resource/img/flame.png')
    boom_image = pg.transform.scale(boom_image, c.size['PLAYER_SIZE'])

    # 미션 4 : 반짝이는 효과를 색반전으로 나타낼 예정
    # 색반전 이미지, 비 색반전 이미지를 분리하여 로드
    non_negative_image = pg.image.load('resource/img/player.png')
    non_negative_image = pg.transform.scale(non_negative_image, c.size['PLAYER_SIZE'])
    negative_image = pg.image.load('resource/img/player_negative.png')
    negative_image = pg.transform.scale(negative_image, c.size['PLAYER_SIZE'])


    def __init__(self, x, y):
        # 처음엔 색반전되지 않은 이미지로 시작
        self.image = Player.non_negative_image

        # 좌표는 각각 [x, y]좌표
        self.pos = [x, y] # 플레이어의 현재 위치(update에 의해 갱신됨)
        self.to = [0, 0] # 플레이어가 이동할 방향(상, 하, 좌, 우, ...)
        self.angle = 0 # 플레이어 각도

        # HP
        self.HP = 5        
        # 무적 현재 무적 시간인지 검사하기 위한 변수
        self.attacked_time = 0 # 피격당한 시각(초 단위)
        self.is_invincible = False # 현재 무적 상태?

        # 색반전으로 무적시간동안 플레이어가 반짝거리도록 조정(스위칭)
        self.now_negative_image = False
        

    # 이상 Player 클래스 기본 설정   
    # ###################################################################
    # 이하 기능 구현 : 렌더링/위치 관련


    # 화면에 플레이어를 렌더링
    def draw(self, screen):
        # 죽은 경우(HP가 0보다 낮아질 수도 있음)
        if self.HP <= 0:
            # 플레이어의 이미지를 폭발하는 이미지로 변경
            self.image = Player.boom_image

        # 무적인 경우
        elif self.is_invincible is True:
            # self.now_negative_image 플래그를 깜빡거리며 색반전/원래 색 플레이어 이미지를 전환
            if self.now_negative_image:
                self.image = Player.non_negative_image
                self.now_negative_image = False
            else:
                self.image = Player.negative_image
                self.now_negative_image = True

        # 무적이 아닌 경우
        # 만약 non_negative_image가 False에 '걸칠'경우 색이 반전되어 플레이어 이미지가 고정됨
        # 따라서 무적이 아닌 경우 항상 플레이어의 이미지를 색이 반전되지 않은 이미지로 고정 
        else :
            self.image = Player.non_negative_image

        # 회전 구현
        if self.to == c.vector['LEFT'] : self.angle = 90
        elif self.to == c.vector['LEFTDOWN'] : self.angle = 135
        elif self.to == c.vector['DOWN'] : self.angle = 180
        elif self.to == c.vector['RIGHTDOWN'] : self.angle = -135
        elif self.to == c.vector['RIGHT'] : self.angle = -90
        elif self.to == c.vector['RIGHTUP'] : self.angle = -45
        elif self.to == c.vector['UP'] : self.angle = 0
        elif self.to == c.vector['LEFTUP'] : self.angle = 45

        rotated_image = pg.transform.rotate(self.image, self.angle)

        calib_pos = (self.pos[0] - c.size['PLAYER_WIDTH']/2,
                     self.pos[1] - c.size['PLAYER_HEIGHT']/2)

        # 화면에 렌더링
        screen.blit(rotated_image, calib_pos)


    # 플레이어의 방향 설정
    def goto(self, x, y):
        self.to[0] += x
        self.to[1] += y


    # 화면상의 플레이어 위치를 업데이트
    def update(self, dt):
        dt = min(Player.SPEED, dt)
        self.pos[0] += dt * self.to[0]
        self.pos[1] += dt * self.to[1]
        # 화면 밖으로 나가지 못하도록 제한
        self.pos[0] = min(max(self.pos[0], c.size['PLAYER_WIDTH']), c.size['SCREEN_WIDTH']-c.size['PLAYER_WIDTH'])
        self.pos[1] = min(max(self.pos[1], c.size['PLAYER_HEIGHT']), c.size['SCREEN_HEIGHT']-c.size['PLAYER_HEIGHT'])
    

    # 이상 기능 구현 : 렌더링/위치 관련
    # ###################################################################
    # 이하 기능 구현 : 충돌 감지/처리 관련


    # 충돌 감지 함수
    def collision(self, bullet):
        if math.sqrt((self.pos[0] - bullet.pos[0])**2 +
                    (self.pos[1] - bullet.pos[1])**2) < 20 :
            return True
        return False


    # * 피격당했을 경우 
    # 1.플레이어의 HP를 총알의 데미지만큼 깎음
    # 2.플레이어가 피격당한 CPU시간을 기록
    # 3.무적상태임을 저장
    # 이걸 다형성이라고 하나? 여하튼 미션 8 커밋을 깜빡해서 주석만 달아놓음(...)
    def attacked(self, bullet):
        # HP가 1씩 떨어지는게 아님!
        self.HP -= bullet.damage
        self.attacked_time = time.time()
        self.is_invincible = True

    # * 피격당했는데 또 맞았을 경우 메인 함수에서 체크함
    def invincible_time_chk(self):
        # 제일 마지막에 피격당한 시간에서 c.INVINCIBLE초 이상 흘렀으면 무적시간이 끝난 것
        if time.time() - self.attacked_time >= Player.INVINCIBLE:
            # 따라서 무적상태 해제
            self.is_invincible = False


    # 이상 기능 구현 : 충돌 감지/처리 관련
    # ###################################################################


# 이상 Player 클래스 
# ###################################################################