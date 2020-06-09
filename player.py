import pygame as pg
import time

from const import Const as c



class Player:
    SPEED = 30
    def __init__(self, x, y):
        self.image = pg.image.load('resource/img/player.png')
        self.image = pg.transform.scale(self.image, c.size['PLAYER_SIZE'])
        # 좌표는 각각 [x, y]좌표
        self.pos = [x, y] # 플레이어의 현재 위치(update에 의해 갱신됨)
        self.to = [0, 0] # 플레이어가 이동할 방향(상, 하, 좌, 우, ...)
        self.angle = 0

        # HP
        self.HP = 5        
        # 무적 시간 : FPS * 5초
        self.invincible_time = 0
        self.is_invincible = False
    
    # 화면에 플레이어를 렌더링
    def draw(self, screen):
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
        screen.blit(rotated_image, calib_pos)

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
    
    # * 피격당했을 경우 
    # 1.플레이어의 HP를 1 깎음
    # 2.플레이어가 피격당한 CPU시간을 기록
    # 3.무적상태임을 저장
    def attacked(self):
        self.HP -= 1
        self.attacked_time = time.time()
        self.is_invincible = True

    # * 피격당했는데 또 맞았을 경우 메인 함수에서 체크함
    def invincible_time_chk(self):
        # 제일 마지막에 피격당한 시간에서 c.INVINCIBLE초 이상 흘렀으면 무적시간이 끝난 것
        if time.time() - self.attacked_time >= c.INVINCIBLE:
            self.is_invincible = False
            return False
        else :
            return True