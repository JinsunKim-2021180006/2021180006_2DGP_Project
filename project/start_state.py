#스타팅 페이지

from pico2d import *
import character_move
import game_framework

stating_image = None

def enter():
    global starting_image
    starting_image = load_image('resource\\background_image_sprites\\Colosseum_of_Fools_Trophy.png')
    pass

def exit():
    global starting_image
    del starting_image
    pass

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_s:
                game_framework.change_state(character_move)
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
        
    pass

def draw():
    clear_canvas()
    starting_image.draw(1270//2,720//2)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass
