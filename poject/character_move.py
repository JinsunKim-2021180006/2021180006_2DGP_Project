from pico2d import *
import game_framework
import loby_state
import start_state
import enemy2_move

frame = 0
spriteNum = 1
DirX, DirY = 0, 0

class Knight:
    def __init__(self):
        self.x,self.y = 0, 110
        self.frame = 0
        self.dir = 1
        self.image = load_image('knight_resource2.png')
    
    def update(self):
        self.frame = (self.frame+1) % spriteNum
        self.x += DirX*5
        self.y += DirY*5
        if self.x > 720:
            self.x = 720
        if self.x<0:
            self.x = 0
        delay(0.01)

    def draw(self):
        self.image.clip_draw(self.frame*80,100*self.dir,80,100,self.x,self.y,80,100)
        
        
knight = None
enemy2_chk = 0

def enter():
    global knight
    knight = Knight()
    pass

def exit():
    global knight
    del knight
    pass

def handle_events():
    global spriteNum, enemy2_chk
    global DirX,DirY
    events = get_events()
    
    for event in events:
        if event.type == SDL_QUIT:
           game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                DirX +=1
                knight.dir = 4
                spriteNum = 9
            elif event.key == SDLK_LEFT:
                DirX -= 1
                knight.dir = 3
                spriteNum = 9
            elif event.key == SDLK_SPACE:
                DirY += 2
            elif event.key == SDLK_ESCAPE:
               game_framework.change_state(start_state)
            
            #적 소환 명령어
            elif event.key == SDLK_e:
                game_framework.push_state(enemy2_move)

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                DirX -=1
                knight.dir = 4
                spriteNum = 1
            elif event.key == SDLK_LEFT:
                DirX += 1
                knight.dir = 3
                spriteNum = 1
            elif event.key == SDLK_SPACE:
                DirY -= 2
            
            
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





#단독 실행 코드
def test_self():
    import sys
    this_module = sys.modules['__main__']

    pico2d.open_canvas(1270,720)
    game_framework.run(this_module)
    pico2d.close_canvas()

if __name__ == '__main__': #만약 단독 실행 상태이면
    test_self()