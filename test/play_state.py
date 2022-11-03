from pico2d import *
import game_framework
import game_world

from character_move import Knight
from arena import Arena


bakcground = None
knight = None

def enter():
    global knight, bakcground
    knight = Knight()
    bakcground = Arena()

    game_world.add_obj(knight,1)
    game_world.add_obj(bakcground,0)

    pass

def exit():
    game_world.clear()
    pass


def update():
    for game_obj in game_world.all_objs():
        game_obj.update()
    pass

def draw_arena():
    for game_obj in game_world.all_objs():
        game_obj.draw()


def draw():
    clear_canvas()
    draw_arena()
    update_canvas()


def pause():
    pass

def resume():
    pass

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

