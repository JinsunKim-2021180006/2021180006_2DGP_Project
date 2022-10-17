from random import random
from re import I
from pico2d import *
import game_framework
import random

frame = 0
spriteNum = 1
move_X, move_Y = 3,2
                       
enemy2s = None
enemy2_num = 1


class Enemy2:
    def __init__(self):
        self.x,self.y = random.randint(100,1190),random.randint(120,620)
        self.frame = 0
        self.dir = 3
        self.image = load_image('resource\\character_image_sprites\\enemy2_resource.png')
    
    def update(self):
        global move_X,move_Y,enemy2_num
        self.frame = (self.frame+1) % spriteNum
        
        if self.x>1270:
            self.dir = 3
            self.x = 1270
            move_X = -move_X
        elif self.x<0:
            self.dir = 1
            self.x = 0  
            move_X = -move_X
            
        if self.y>720:
            self.y = 720
            move_Y = -move_Y
        elif self.y<110:
            self.y = 110
            move_Y = -move_Y
        self.x += move_X
        self.y += move_Y
           

      
        delay(0.01)

    def draw(self):
        self.image.clip_draw(self.frame*500,600*self.dir,500,600,self.x,self.y,100,120)
        
 
def enter():
    global enemy2s, enemy2_num
    if enemy2_num<=0:
        enemy2_num=0
    enemy2s = [Enemy2()for i in range(0,enemy2_num)]
   
    pass

def exit():
    global enemy2s
    del enemy2s
    pass

def handle_events():
    global enemy2_num
    events = get_events()

    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_e:
                enemy2_num += 1
            elif event.key == SDLK_ESCAPE:
                game_framework.pop_state()
    pass

def draw():
    clear_canvas()
    for enemy2 in enemy2s:
        enemy2.draw()
    update_canvas()

def update():
    for enemy2 in enemy2s:
        enemy2.update()
    pass

def pause():
    pass

def resume():
    pass




#단독 실행 코드
def test_self():
    import sys
    this_module = sys.modules['__main__']

    pico2d.open_canvas(1270,720)
    game_framework.run(this_module)
    pico2d.close_canvas()

if __name__ == '__main__': #만약 단독 실행 상태이면
    test_self()