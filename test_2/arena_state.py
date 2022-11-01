from pico2d import *
import game_framework
from character_move import Knight

image = None
DirX,DirY=0,0

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
    knight.update(DirX,DirY)
    pass

def draw_arena():
    image.draw(1270//2,720//2)
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
    global DirX,DirY

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
            game_framework.quit()
        else:
            knight.handle_event(event)


    #     if event.type == SDL_KEYDOWN:
    #         if event.key == SDLK_ESCAPE:
    #             game_framework.quit()

    #         elif event.key == SDLK_RIGHT:
    #             DirX +=1
    #             knight.dir = 4
    #             character_move.spriteNum = 9
    #         elif event.key == SDLK_LEFT:
    #             DirX -= 1
    #             knight.dir = 3
    #             character_move.spriteNum = 9
    #         elif event.key == SDLK_s:
    #             if knight.dir == 4:
    #                 DirX+=3
    #             elif knight.dir == 3:
    #                 DirX-=3



    #     elif event.type == SDL_KEYUP:
    #         if event.key == SDLK_RIGHT:
    #             DirX -=1
    #             knight.dir = 4
    #             character_move.spriteNum = 1
    #         elif event.key == SDLK_LEFT:
    #             DirX += 1
    #             knight.dir = 3
    #             character_move.spriteNum = 1
    #         elif event.key == SDLK_s:
    #             if knight.dir == 4:
    #                 DirX-=3
    #             elif knight.dir == 3:
    #                 DirX+=3

    pass

