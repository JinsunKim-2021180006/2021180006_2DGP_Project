from pico2d import *
import game_framework
import character_move


loby_image = None

def enter():
    global loby_image
    loby_image = load_image('Colosseum_Lobby.png')
    pass

def exit():
    global loby_image
    del loby_image
    pass

def handle_events():
    events = get_events()
        
    pass

def draw():
    clear_canvas()
    loby_image.draw(1270//2,720//2)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass






