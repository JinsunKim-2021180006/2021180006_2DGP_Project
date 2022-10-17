#로비
from pico2d import *
import game_framework
import start_state


loby_image = None

def enter():
    global loby_image
    loby_image = load_image('resource\\background_image_sprites\\Colosseum_Lobby.png')
    pass

def exit():
    global loby_image
    del loby_image
    pass

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(start_state)
        
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






