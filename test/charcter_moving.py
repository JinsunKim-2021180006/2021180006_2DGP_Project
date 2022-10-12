#2022-10-12
#수정&추가해야하는 사항들은 주석으로 표시
#배경 띄우기, 캐릭터 이동 모션 확인용
# 캐릭터 사이즈 80*100



from pickle import FALSE
from winreg import DisableReflectionKey
from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 1920, 1080 #화면 사이즈

def handle_events():
    global moving
    global x,y
    global ground, direction, spriteNum
    global mainDirX, mainDirY

    global BossDir, BossSprNum

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            moving = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                mainDirX +=1
                direction = 4
                spriteNum = 9
            elif event.key == SDLK_LEFT:
                mainDirX -= 1
                direction = 3
                spriteNum = 9
            elif event.key == SDLK_SPACE:
                mainDirY += 2
            elif event.key == SDLK_ESCAPE:
                moving = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mainDirX -=1
                direction = 4
                spriteNum = 1
            elif event.key == SDLK_LEFT:
                mainDirX += 1
                direction = 3
                spriteNum = 1
            elif event.key == SDLK_SPACE:
                mainDirY -= 2

    pass


open_canvas(CANVAS_WIDTH,CANVAS_HEIGHT)

BG_Arena = load_image('Colosseum_Arena.png')
character = load_image('knight_resource2.png')
Boss1 = load_image('Boss1_resource.png')

moving = True
ground = 175 # 바닥 위치
x,y = CANVAS_WIDTH//2, ground
main_frame = 0
mainDirX, mainDirY = 0,0

# 4 = 오른쪽 달리기 
# 3 = 왼쪽 달리기
# 1,2 = 공격
# 0 = 점프모션
direction = 4
# 출력할 스프라이트 개수
spriteNum = 1

#========================================
BossDir = 1
BossSprNum = 6
Boss_frame = 0

BossX,BossY = 500,ground+300

hide_cursor()

while moving:
    clear_canvas()
    BG_Arena.draw(CANVAS_WIDTH//2,CANVAS_HEIGHT//2)
    character.clip_draw(main_frame*80,100*direction,80,100,x,y,90,110)
    Boss1.clip_draw(Boss_frame*500,500*BossDir,500,500,BossX,BossY,300,300)
    update_canvas()
    handle_events()
    main_frame = (main_frame+1) % spriteNum
    Boss_frame = (Boss_frame+1) % BossSprNum
    x += mainDirX*6
    y += mainDirY*10
    delay(0.03)

close_canvas()