from pico2d import *
import play_state
import game_framework

stating_image = None
stating_sound = None

def enter():
    global starting_image, stating_sound
    starting_image = load_image('resource\\background_image_sprites\\Colosseum_of_Fools_Trophy.png')
    stating_sound = load_wav('resource\\sound\\start_state.wav')
    stating_sound.set_volume(32)
    pass

def exit():
    global starting_image
    del starting_image
    pass

def handle_events():
    global stating_sound
    events = get_events()

    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_s:
                stating_sound.play()
                delay(1.5)
                game_framework.change_state(play_state)
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
