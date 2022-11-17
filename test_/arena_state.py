from pico2d import *
import game_framework
from Knight import Knight


MAP_SIZE_width = 1270
MAP_SIZE_height = 720
image = None


def enter():
    global image, knight
    knight = Knight()
    image = load_image('resource\\background_image_sprites\\Colosseum_Arena.png')
    
    pass

def exit():
    global image,knight
    del image,knight
    pass


def update():
    knight.update()
    pass

def draw_arena():
    image.draw(MAP_SIZE_width // 2,MAP_SIZE_height//2)
    knight.draw()

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

