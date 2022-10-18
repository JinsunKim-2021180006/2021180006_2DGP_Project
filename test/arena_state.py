from pico2d import *
import game_framework
import character_move
import loby_state

image = None
DirX,DirY=0,0

def enter():
    global image,knight
    knight = character_move.Knight(10,110)
    image = load_image('resource\\background_image_sprites\\Colosseum_Arena.png')
    
    pass

def exit():
    global image,knight
    del image,knight
    pass

def handle_events():
    global DirX,DirY

    events = get_events()

    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()

            elif event.key == SDLK_RIGHT:
                DirX +=1
                knight.dir = 4
                character_move.spriteNum = 9
            elif event.key == SDLK_LEFT:
                DirX -= 1
                knight.dir = 3
                character_move.spriteNum = 9
            elif event.key == SDLK_s:
                if knight.dir == 4:
                    DirX+=3
                elif knight.dir == 3:
                    DirX-=3



        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                DirX -=1
                knight.dir = 4
                character_move.spriteNum = 1
            elif event.key == SDLK_LEFT:
                DirX += 1
                knight.dir = 3
                character_move.spriteNum = 1
            elif event.key == SDLK_s:
                if knight.dir == 4:
                    DirX-=3
                elif knight.dir == 3:
                    DirX+=3


    del events
    pass

def draw():
    clear_canvas()
    image.draw(1270//2,720//2)
    knight.draw()
    update_canvas()

def update():
    global DirX,DirY,knight
    knight.update(DirX,DirY)    
    if knight.x<=0:
        game_framework.change_state(loby_state)
    pass

def pause():
    pass

def resume():
    pass


