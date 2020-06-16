# 전 파일에 거쳐 사용할 변수를 관리하는 클래스

class Const:
    # FPS
    FPS = 60
    # 무적시간
    INVINCIBLE = 2

    # 초당 생성되는 새 총알의 갯수
    DIFFICULTY = 1

    # RGB코드
    color = {
        'BLACK':(0, 0, 0),
        'WHITE':(255, 255, 255),
        'YELLOW':(255, 255, 0),
        'RED':(255, 0, 0),
        'BLUE':(0, 0, 255),
        'GREY':(224, 224, 224),

        # 배터리 칸에 각각 사용될 RGB코드
        'BATTERY':[(239,69,54),
            (251,176,64),
            (248,237,60),
            (141,198,63),
            (69,149,68)
        ][::-1]
    }
    
    # 객체 크기
    size = {
        # 메인 화면
        'SCREEN_WIDTH':1000,
        'SCREEN_HEIGHT':800,
        'SCREEN_SIZE':(1000, 800),

        # 플레이어
        'PLAYER_WIDTH':64,
        'PLAYER_HEIGHT':64,
        'PLAYER_SIZE':(64, 64),

        # 총알
        'BULLET_RADIUS':7,
        'WEAK_BULLET_RADIUS':16,
        'NORMAL_BULLET_RADIUS':8,
        'STRONG_BULLET_RADIUS':4,
    }

    vector = {
        'LEFT':[-1, 0],
        'RIGHT':[1, 0],
        'DOWN':[0, 1],
        'UP':[0, -1],
        'LEFTUP':[-1, -1],
        'RIGHTUP':[1, -1],
        'LEFTDOWN':[-1, 1],
        'RIGHTDOWN':[1, 1]
    }
    
    