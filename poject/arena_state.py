from pico2d import *
import game_framework


arena_image = None

def enter():
    global arena_image
    arena_image = load_image('Colosseum_Arena.png')
    pass

def exit():
    global arena_image
    del arena_image
    pass

def handle_events():
    events = get_events()
        
    pass

def draw():
    clear_canvas()
    arena_image.draw(1270//2,720//2)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass





