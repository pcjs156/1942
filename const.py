class Const:
    FPS = 60
    INVINCIBLE = 0.5

    # 1이 기본, 클수록 어려움(초당 총알 갯수)
    DIFFICULTY = 1

    color = {
        'BLACK':(0, 0, 0),
        'WHITE':(255, 255, 255),
        'YELLOW':(255, 255, 0),
        'RED':(190, 0, 0)
    }
    
    size = {
        'SCREEN_WIDTH':1000,
        'SCREEN_HEIGHT':800,
        'SCREEN_SIZE':(1000, 800),

        'PLAYER_WIDTH':64,
        'PLAYER_HEIGHT':64,
        'PLAYER_SIZE':(64, 64),

        'BULLET_RADIUS':7,
        'SCOREBOARD_SIZE':32,
        'GAMEOVER_SIZE':100
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
    
    