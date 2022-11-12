from pico2d import *
from random import randint
import game_framework
import game_world


from arena import Arena
from Knight import Knight
from enemy2 import Enemy2
from Block import Block, Wall


MAP_SIZE_width = 1270
MAP_SIZE_height = 720

knight = None
enemy2 = None

block = None
wall = None
background_img = None

coliBox = False

def handle_events():
    global coliBox
    events = 0
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_p):
            if coliBox:
                coliBox = False
            else:
                coliBox = True
        else:
            knight.handle_event(event)
    pass


def enter():
    global knight, enemy2 ,background_img, block, wall
    print("enter loby state")
    
    knight = Knight()
    game_world.add_obj(knight,1)
    
    enemy2 = [Enemy2() for n in range(15)]
    game_world.add_objs(enemy2,1)

    background_img = Arena(MAP_SIZE_width,MAP_SIZE_height)
    game_world.add_obj(background_img,0)
    
    block = [Block(randint(200,1000),randint(300,600)) for n in range(10)]
    wall = Wall(-5,1100)
    game_world.add_objs(block, 0)
    game_world.add_obj(wall, 0)

    game_world.add_collision_group(knight,background_img,'knight:ground')
    game_world.add_collision_group(knight,block,'knight:ground')

   
    pass

def exit():
    game_world.clear()
    pass

def update():
    global BG_state, background_img

    for game_obj in game_world.all_objs():
        game_obj.update()
        

    for a,b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('COLLID by ', group)
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


