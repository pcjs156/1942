# RankingProcessor 클래스와 텍스트 렌더링 함수 정의

import pickle
import os
import time

import pygame as pg
from const import Const as c

# 이상 모듈/클래스 import 
# ###################################################################
# 이하 텍스트 렌더링 함수

def draw_text(screen, txt, size, pos, color):
    font = pg.font.Font('resource/fonts/LinLibertine_RZ.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)

# 이상 텍스트 렌더링 함수
# ###################################################################
# 이하 토큰 발급 함수
# : 기록 정보를 서로 구분하기 위함(동점자 등)
# : 랭킹 정보 발급 시간(time())으로 부여
# : Python이 Stable한 정렬을 하기 때문에 순위 내에 동점자가 있을 경우
# : 먼저 등록된 플레이어의 기록만 10위권에 표시된다. 나머지는 잘림.

def get_token():
    return int(time.time())

# 이상 토큰 발급 함수
# ###################################################################
# 이하 RankingProcessor클래스
# : 주로 파일을 pickle의 형태로 읽고, 쓰고, 사용하는 역할


# 미션 9 : 사용자의 가장 오래 버틴 생존 시간을 최대 10개까지 파일에 기록한다.
class RankingProcessor:
    # ###################################################################
    # 이하 RankingProcessor 클래스 기본 설정

    def __init__(self, filename):
        self.filename = filename

        # 파일의 유무를 먼저 파악해 파일이 없을 경우 만들어줌
        self.chk_ranking_file(self.filename)
        self.records = self.load_ranking_file()


    # 이상 RankingProcessor 클래스 기본 설정   
    # ###################################################################
    # 이하 기능 구현 : pickle 관련


    # filename이 해당 디렉토리에 존재하지 않을 경우 새로 만들어줌
    # .gitignore에서 'ranking'이라는 이름의 파일을 스테이징 대상에서 제외함
    def chk_ranking_file(self, filename:str):
        if filename not in os.listdir():
            with open(filename, 'wb') as f:
                print("{}이 존재하지 않아 새로 생성합니다.".format(filename))


    # 랭킹 정보가 담긴 파일을 리스트로 변환하여 반환해줌
    def load_ranking_file(self)->list:
        f = open(self.filename, 'rb')
        try:
            # 파일로부터 데이터 가져오기
            data = pickle.load(f)
        except EOFError:
            # 파일에 아무 것도 저장되어 있지 않은 경우,
            # 기록이 없다는 의미이므로 빈 리스트를 리턴해주면 됨
            data = list()
        finally:
            # 파일 닫아주기
            f.close()
        
        return data

    # 개임 내에서 기록을 0.1초 단위로 기록하므로
    # 기록을 저장할 때는 소숫점 아래 1자리까지 표현하는 str로 저장(2번째 자리에서 반올림)
    def add_to_ranking_file(self, new_record, token):
        # 랭킹 정보 추가(소수점 아래 2번째에서 반올림해줌)
        self.records.append(("{:0.1f}".format(round(new_record, 1)), token))
        # 랭킹 정렬(내림차순)
        self.records.sort(key=lambda r: float(r[0]), reverse=True)
        
        # 상위기록 10개를 제외한 나머지 기록을 버림
        self.records = self.records[:10]

        # 기존 파일에 쓰기
        with open(self.filename, 'wb') as f:
            pickle.dump(self.records, f)
        

    # 이상 기능 구현 : pickle 관련
    # ###################################################################
    # 이하 기능 구현 :점수판 렌더링


    # 점수판 렌더링
    def render_ranking_board(self, screen, token):
        width, height = screen.get_size()
        board_width, board_height = width * 0.3, height * 0.45
        
        # 점수판 배경으로 쓸 사각형 렌더링 
        pg.draw.rect(screen, c.color['GREY'], [width/2-board_width/2-5, 250, board_width, board_height])

        # 렌더링
        for i in range(len(self.records)):
            # 이번에 입력된 기록(records)의 토큰과 현재 기록의 토큰이 같으면 이번에 순위권에 들어갔다는 의미
            # 따라서 붉은 색으로 강조 
            font_color = c.color['RED'] if self.records[i][1] == token else c.color['BLACK']
            
            # 등수 렌더링 : 1~3등을 제외한 나머지 4~10등은 뒤에 th를 붙임
            if i == 0 :
                rank = "1st"
            elif i == 1 :
                rank = "2nd"
            elif i == 2 :
                rank = "3rd"
            else :
                rank = str(i+1) + "th"
            draw_text(screen, "{:>5}".format(rank), 40, (width/2-board_width/2+50, 270 + 30 * i), font_color)

            # 점수 렌더링 : 토큰으로 구별
            draw_text(screen, "{:>6}".format(self.records[i][0]), 40, (width/2-board_width/2+140, 270 + 30 * i), font_color)


    # 이상 기능 구현 :점수판 렌더링
    # ###################################################################

# 이상 RankingProcessor 클래스 
# ################################################################### 