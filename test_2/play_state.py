from pico2d import *
import game_framework
import game_world

from arena import Arena
from character_move import Knight

MAP_SIZE_width = 1270
MAP_SIZE_height = 720

knight = None

# 0 = loby, 1 = hall, 2 = arena
background_state = 0 
background_img = None


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
            game_framework.quit()
        else:
            knight.handle_event(event)

    pass


def enter():
    global knight, background_img
    knight = Knight()
    background_img = Arena(MAP_SIZE_width,MAP_SIZE_height)

    game_world.add_obj(knight,1)
    game_world.add_obj(background_img,0)

    pass

def exit():
    game_world.clear()
    pass

def update():
    for game_obj in game_world.all_objs():
        game_obj.update()
    pass

def draw_world():
    for game_obj in game_world.all_objs():
        game_obj.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def pause():
    pass

def resume():
    pass


