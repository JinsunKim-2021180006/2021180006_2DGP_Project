#로비
from pico2d import *
import game_framework
import character_move
import arena_state
import enemy2_move

loby_image = None
DirX,DirY=0,0
enemy2_num = 0

def enter():
    global loby_image,knight,enemy2_num,enemy2
    knight = character_move.Knight(1250,110)
    
    loby_image = load_image('resource\\background_image_sprites\\Colosseum_Lobby.png')
    
    pass

def exit():
    global loby_image,knight
    del loby_image,knight
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
            elif event.key == SDLK_e:
                enemy2_num+=1

    pass

def draw():
    clear_canvas()
    enemy2 = [enemy2_move.Enemy2()for i in range(0,enemy2_num)]
    loby_image.draw(1270//2,720//2)
    knight.draw()
    enemy2.draw()
    update_canvas()

def update():
    global DirX,DirY
    knight.update(DirX,DirY)
    enemy2.update()
    if knight.x>=1270:
        game_framework.change_state(arena_state)


    pass

def pause():
    pass

def resume():
    pass






