from pico2d import *

RD,LD,RU,LU = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
}

spriteNum = 1

class IDLE:
    @staticmethod
    def enter(self,event):
        self.dir = 0
    
    def exit(self):
        pass

    def do(self):
        self.frame = (self.frame+1)%spriteNum
        pass

    def draw(self):
        self.image.clip_draw(self.frame*80,100*self.dir,80,100,self.x,self.y,80,100)

class moving:
    def enter(self,event):
        pass    

class Knight:
    def __init__(self,x,y):
        self.x,self.y = x, y
        self.frame = 0
        self.dir = 1
        self.image = load_image('resource\\character_image_sprites\\knight_resource2.png')
    
        self.event_que  = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self,DirX,DirY):
        global state_chk

        self.frame = (self.frame+1) % spriteNum
        self.x += DirX*5
        self.y += DirY*5

        if self.x >= 1270:
            self.x = 1270
        elif self.x <= 0:
            self.x = 0


        delay(0.01)

    def draw(self):
        self.image.clip_draw(self.frame*80,100*self.dir,80,100,self.x,self.y,80,100)