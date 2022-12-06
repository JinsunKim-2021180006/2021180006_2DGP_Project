from pico2d import *
import game_framework
import game_world
import start_state
import arena_state
import GUI

from background import Arena, Hall, Loby, END
from Knight import Knight
from enemy import Enemy2, Enemy1, Boss
from Block import Block, Wall

from source import knight,enemy1,enemy2,boss,spirit,\
    door_up,door_down,door_updown

MAP_SIZE_width = 1270
MAP_SIZE_height = 720

# 배경 관련
# 0 = loby, 1 = hall, 2 = arena, 3 =end
BG_state = 0
background_img = None

#Bool함수들
coliBox = False #충돌박스 on/off
fighting_on = False #아레나 전투 on/off

# arena 관련
F1,F2 = [], []
wall = None
level_chk = 0

enemy_cnt = 1

def handle_events():
    global coliBox
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
            if not BG_state == 2: # arena에서는 안됨
                game_framework.change_state(start_state)
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_p):
            if coliBox:
                coliBox = False
            else:
                coliBox = True
        else:
            knight.handle_event(event)
    pass


def enter():
    global knight, background_img,wall,enemy2,enemy1,boss,spirit
    print("enter loby state")
    
    #배경 오브젝트
    background_img = Loby(MAP_SIZE_width,MAP_SIZE_height)
    game_world.add_obj(background_img,0)
    
    #캐릭터 
    knight = Knight()
    game_world.add_obj(knight,1)

    knight.Gui()
    pass

def exit():
    game_world.clear()
    pass

def update():
    global BG_state, background_img, fighting_on,knight,enemy_cnt

    
    for game_obj in game_world.all_objs():
        game_obj.update()
    if not fighting_on:
        if knight.x == 1270: # 맵 우측 끝으로 가면
            game_world.remove_obj(background_img) #더블 버퍼링
            if BG_state == 0: # 로비->복도
                knight.x = 1
                BG_state = 1
                background_img = Hall(MAP_SIZE_width,MAP_SIZE_height)
            elif BG_state == 1: # 복도-> 아레나
                knight.x = 1
                BG_state = 2
                background_img = Arena(MAP_SIZE_width,MAP_SIZE_height)
            game_world.add_obj(background_img,0)

        elif knight.x == 0: # 맵 좌측 끝으로 가면
            game_world.remove_obj(background_img)
            if BG_state == 1: # 로비 <-복도 
                knight.x = 1270
                BG_state = 0
                background_img = Loby(MAP_SIZE_width,MAP_SIZE_height)
            elif BG_state == 2: # 복도 <- 아레나
                if not fighting_on:
                    knight.x = 1270
                    BG_state = 1
                    background_img = Hall(MAP_SIZE_width,MAP_SIZE_height)
            game_world.add_obj(background_img,0)
        
        elif knight.x >= 200:
            if BG_state == 2: #만약 아레나 안쪽으로 충분히 들어온다면 -> fighting_start
                if not fighting_on :
                    fighting()
    

    if enemy_cnt == 0:
        game_world.remove_obj(background_img)
        BG_state = 3
        background_img = END(MAP_SIZE_width,MAP_SIZE_height)
        game_world.add_obj(background_img,1)
        enemy_cnt = 1

    for a,b, group in game_world.all_collision_pairs():
        if collide(a, b):
            a.handle_collision(b, group)
            b.handle_collision(a, group)

    pass

def draw_world():
    for game_obj in game_world.all_objs():
        game_obj.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def collide(a,b):
    la,ba,ra,ta = a.get_bb()
    lb,bb,rb,tb = b.get_bb()

    if la > rb : return False
    if ra < lb : return False
    if ta < bb : return False
    if ba > tb : return False

    return True

def pause():
    pass

def resume():
    pass


def fighting():
    global fighting_on,level_chk, enemy1,enemy2,door_up,door_updown,door_down

    fighting_on = True

    wall = Wall(-5,1100)
    game_world.add_obj(wall, 0)
    setPlatform()
    level_chk = 1
    door_up= GUI.Door(1200,140,0)
    game_world.add_obj(door_up,0)
    door_updown= GUI.Door(1200,320,1)
    game_world.add_obj(door_updown,0)

    door_down= GUI.Door(1200,620,2)
    game_world.add_obj(door_down,0)

    delay(1)
    #level1 start 
    if level_chk == 1:
        level1()
    
    game_world.add_collision_group(spirit,enemy1, 'spirit:enemy')
    game_world.add_collision_group(spirit,enemy2, 'spirit:enemy')

    game_world.add_collision_group(knight,enemy1,'knight:enemy')
    game_world.add_collision_group(knight,enemy2,'knight:enemy')
    
    game_world.add_collision_group(knight,door_down,'knight:down')
    game_world.add_collision_group(knight,door_updown,'knight:updown')
    game_world.add_collision_group(knight,door_up,'knight:up')


def level1():
    global enemy1,enemy2,boss,enemy_cnt

    enemy_cnt = 6

    enemy2 = [Enemy2() for n in range(4)]
    game_world.add_objs(enemy2,1)
    enemy1 = [Enemy1(290) for n in range(2)]
    game_world.add_objs(enemy1,1)
    pass
    
def setPlatform():
    global F1,F2
    block_list = [80,190,300,410,520,630,740,850,960,1070,1180,1290]
    
    i = 0
    for i in range(12):
        F1 = [Block(block_list[i],250)]
        game_world.add_objs(F1, 0)

    for i in range(12):
        F2 = [Block(block_list[i],550)]
        game_world.add_objs(F2, 0)
