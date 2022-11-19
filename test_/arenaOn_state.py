from pico2d import *
from random import randint
import game_framework
import game_world


from arena import Arena
from Knight import Knight
from enemy import Enemy2, Enemy1
from Block import Block, Wall
from GUI import HP

MAP_SIZE_width = 1270
MAP_SIZE_height = 720

knight = None
enemy1 = None
enemy2 = None
hp = None

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
    
    enemy2 = [Enemy2() for n in range(2)]
    game_world.add_objs(enemy2,1)
    enemy1 = [Enemy1() for n in range(3)]
    game_world.add_objs(enemy1,1)

    background_img = Arena(MAP_SIZE_width,MAP_SIZE_height)
    game_world.add_obj(background_img,0)
    

    setPlatform()
    wall = Wall(-5,1100)
    game_world.add_obj(wall, 0)

    knight.GUI()

    game_world.add_collision_group(knight,background_img,'knight:ground')
    game_world.add_collision_group(knight,block,'knight:ground')

    game_world.add_collision_group(enemy2,background_img,'enemy2:ground')
    game_world.add_collision_group(enemy2,block,'enemy2:ground')

    game_world.add_collision_group(enemy1,knight,'enemy1:obj')

    game_world.add_collision_group(knight,enemy1,'knight:enemy')
    game_world.add_collision_group(knight,enemy2,'knight:enemy')
   
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

def setPlatform():
    
    block_list = [80,190,300,410,520,630,740,850,960,1070,1180,1290]
    
    i = 0
    for i in range(12):
        block = [Block(block_list[i],250) for n in range(1)]
        game_world.add_objs(block, 0)


    for i in range(12):
        block = [Block(block_list[i],550)]
        game_world.add_objs(block, 0)

