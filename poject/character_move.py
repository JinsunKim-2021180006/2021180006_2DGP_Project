from pico2d import *
import game_framework
import loby_state
import start_state

frame = 0
spriteDir = 1
spriteNum = 1
DirX, DirY = 0,0

class Knight:
    def __init__(self):
        self.x,self.y = 1270//2, 175
        self.frame = 0
        self.dir = 1
        self.image = load_image('knight_resource2.png')
    
    def update(self):
        self.frame = (self.frame+1) % spriteNum
        self.x += DirX*3
        self.y += DirY*5
        delay(0.01)

    def draw(self):
        self.image.clip_draw(self.frame*80,100*spriteDir,80,100,self.x,self.y,80,100)
        
        
knight = None

def enter():
    global knight
    knight = Knight()
    pass

def exit():
    global knight
    del knight
    pass

def handle_events():
    global spriteDir, spriteNum
    global DirX,DirY
    events = get_events()
    
    for event in events:
        if event.type == SDL_QUIT:
           game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                DirX +=1
                spriteDir = 4
                spriteNum = 9
            elif event.key == SDLK_LEFT:
                DirX -= 1
                spriteDir = 3
                spriteNum = 9
            elif event.key == SDLK_SPACE:
                DirY += 2
            elif event.key == SDLK_ESCAPE:
               game_framework.change_state(start_state)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                DirX -=1
                spriteDir = 4
                spriteNum = 1
            elif event.key == SDLK_LEFT:
                DirX += 1
                spriteDir = 3
                spriteNum = 1

    pass

def draw():
    clear_canvas()
    loby_state.enter()
    loby_state.draw()
    knight.draw()
    update_canvas()

def update():
    knight.update()
    pass

def pause():
    pass

def resume():
    pass





