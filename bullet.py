# 총알 클래스

import pygame as pg
import random as rnd

from const import Const as c


# 이상 모듈/클래스 import 
# ###################################################################
# 이하 Bullet 클래스

class Bullet:
    # ###################################################################
    # 이하 Bullet 클래스 기본 설정 / staticmethod
    
    # 게임을 시작할 때 생성할 총알 갯수
    initial_bullet_cnt = 10

    # 약, 중, 강 총알의 비율을 4 : 2 : 1로 정함(확률 구현)
    bullet_box = ['w'] * 4 + ['n'] * 2 + ['h'] * 1
    # 4/7, 2/7, 1/7확률로 랜덤하게 각각의 총알 인스턴스를 생성하여 반환
    @staticmethod
    def return_random_bullet(x, y, to_x, to_y):
        pick = rnd.choice(Bullet.bullet_box)
        
        if pick == 'w':
            return WeakBullet(x, y, to_x, to_y)
        if pick == 'n':
            return NormalBullet(x, y, to_x, to_y)
        else:
            return StrongBullet(x, y, to_x, to_y)


    def __init__(self, x, y, to_x, to_y):
        # 좌표는 각각 [x, y]좌표
        self.pos = [x, y]
        self.to = [to_x, to_y]
        # 총알의 크기와 색은 Bullet클래스를 상속받는 클래스에서 재정의할 것
        self.radius = None
        self.color = None
        self.damage = 0
    
    # 이상 Player 클래스 기본 설정 / staticmethod
    # ###################################################################
    # 이하 기능 구현 : 렌더링/위치 관련

    def update_and_draw(self, dt, screen):
        self.pos[0] = (self.pos[0] + dt*self.to[0]) % c.size['SCREEN_WIDTH']
        self.pos[1] = (self.pos[1] + dt*self.to[1]) % c.size['SCREEN_HEIGHT']

        pos_int = (int(self.pos[0]), int(self.pos[1]))
        pg.draw.circle(screen, self.color, pos_int, self.radius)
    
    # 이상 기능 구현 : 렌더링/위치 관련
    # ###################################################################

# 이상 Bullet 클래스
# ###################################################################
# 이하 Bullet 클래스를 상속받은 자식 클래스들
    

# self.color, self.radius, self.damage가 각각의 값을 재정의
class WeakBullet(Bullet):
    def __init__(self, x, y, to_x, to_y):
        super().__init__(x, y, to_x, to_y)
        self.radius = c.size['WEAK_BULLET_RADIUS']
        self.color = c.color['YELLOW']
        self.damage = 1

class NormalBullet(Bullet):
    def __init__(self, x, y, to_x, to_y):
        super().__init__(x, y, to_x, to_y)
        self.radius = c.size['NORMAL_BULLET_RADIUS']
        self.color = c.color['WHITE']
        self.damage = 2

class StrongBullet(Bullet):
    def __init__(self, x, y, to_x, to_y):
        super().__init__(x, y, to_x, to_y)
        self.radius = c.size['STRONG_BULLET_RADIUS']
        self.color = c.color['RED']
        self.damage = 3


# 이상 Bullet 클래스를 상속받은 자식 클래스들
# ###################################################################