from pico2d import *
import game_framework
import game_world
import start_state
import arena_state

from background import Arena, Hall, Loby
from Knight import Knight

MAP_SIZE_width = 1270
MAP_SIZE_height = 720

knight = None
bgm = None

# 0 = loby, 1 = hall, 2 = arena
BG_state = 0
background_img = None

coliBox = False

def handle_events():
    global coliBox
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
            game_framework.change_state(start_state)
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_p):
            if coliBox:
                coliBox = False
            else:
                coliBox = True
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_0):
            game_framework.change_state(arena_state)
        else:
            knight.handle_event(event)
    pass


def enter():
    global knight, background_img,bgm
    print("enter loby state")
    knight = Knight()
    background_img = Loby(MAP_SIZE_width,MAP_SIZE_height)

    bgm = load_music('resource\\sound\\loby_bgm.mp3')
    bgm.set_volume(60)
    bgm.repeat_play()

    game_world.add_obj(knight,1)
    game_world.add_obj(background_img,0)

    game_world.add_collision_group(knight,background_img,'knight:ground')
    game_world.add_collision_group(knight,background_img,'knight:ground')

    pass

def exit():
    game_world.clear()
    pass

def update():
    global BG_state, background_img

    
    for game_obj in game_world.all_objs():
        game_obj.update()

    if knight.x == 1270:
        game_world.remove_obj(background_img)
        if BG_state == 0:
            knight.x = 1
            BG_state = 1
            background_img = Hall(MAP_SIZE_width,MAP_SIZE_height)
        elif BG_state == 1:
            knight.x = 1
            BG_state = 2
            background_img = Arena(MAP_SIZE_width,MAP_SIZE_height)
        game_world.add_obj(background_img,0)
    elif knight.x == 0:
        game_world.remove_obj(background_img)
        if BG_state == 1:
            knight.x = 1270
            BG_state = 0
            background_img = Loby(MAP_SIZE_width,MAP_SIZE_height)
        elif BG_state == 2:
            knight.x = 1270
            BG_state = 1
            background_img = Hall(MAP_SIZE_width,MAP_SIZE_height)
        game_world.add_obj(background_img,0)
    elif knight.x >= 100:
        if BG_state == 2:
            #만약 아레나 안쪽으로 들어온다면 -> arenaOn_state
            knight.dir = 0
            game_framework.change_state(arena_state)
            pass

        

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


