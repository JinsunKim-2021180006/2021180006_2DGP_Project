#2022-10-11
#수정&추가해야하는 사항들은 주석으로 표시
#배경 띄우기, 캐릭터 이동 모션 확인용
# 캐릭터 사이즈 79*78


########## 수정해야하는 부분 #########
# frame = (frame+1)%변수(출력하는 스프라이트 수) + 변수(스프라이트에서 출력하는 라인)


from pickle import FALSE
from winreg import DisableReflectionKey
from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 1920, 1080 #화면 사이즈

def handle_events():
    global moving
    global x,y
    global ground
    global mainDirX, mainDirY

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            moving = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                mainDirX +=1
            elif event.key == SDLK_LEFT:
                mainDirX -= 1
            elif event.key == SDLK_SPACE:
                mainDirY += 2
            elif event.key == SDLK_ESCAPE:
                moving = False
        # elif event.type == SDL_KEYUP:
        #     if event.key == SDLK_RIGHT:
        #         mainDirX -=1
        #     elif event.key == SDLK_LEFT:
        #         mainDirX += 1
        #     elif event.key == SDLK_SPACE:
        #         mainDirY -= 2

    pass


open_canvas(CANVAS_WIDTH,CANVAS_HEIGHT)

BG_Arena = load_image('Colosseum_Arena.png')
character = load_image('knight_resource1.webp')

moving = True
ground = 190 # 바닥 위치
x,y = CANVAS_WIDTH//2, ground
main_frame = 0
mainDirX, mainDirY = 0,0
direction = 0

hide_cursor()

while moving:
    clear_canvas()
    BG_Arena.draw(CANVAS_WIDTH//2,CANVAS_HEIGHT//2)
    character.clip_draw(main_frame*79,78*6,79,78,x,y,90,90)
    update_canvas()
    handle_events()
    main_frame = (main_frame+1)%6 +6
    x += mainDirX*6
    y += mainDirY*10
    delay(0.03)

close_canvas()