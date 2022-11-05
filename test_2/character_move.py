from pico2d import *

RD,LD,RU,LU,JUMP_u,JUMP_d, Shift_d,Shift_u = range(8)

event_name = ['RD', 'LD', 'RU', 'LU','JUMP_u','JUMP_d','DASH']


key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    
    (SDL_KEYDOWN,SDLK_SPACE): JUMP_d,
    (SDL_KEYUP,SDLK_SPACE): JUMP_u,

    (SDL_KEYDOWN, SDLK_LSHIFT): Shift_d,
    (SDL_KEYUP, SDLK_LSHIFT): Shift_u
}


class IDLE:
    @staticmethod
    def enter(self,event):
        self.dir = 0

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame+1)% 1
        pass
    
    @staticmethod
    def draw(self):
        self.image.clip_draw(self.frame*80,100*self.face,80,100,self.x,self.y,80,100)

class MOVING:
    def enter(self,event):
        if event == RD:
            self.dir +=1
            self.face = 4
            self.spriteNum = 9
        elif event == LD:
            self.dir -=1
            self.face = 3
            self.spriteNum = 9
        elif event == RU:
            self.dir -=1
            self.face = 4
            self.spriteNum = 1
        elif event == LU:
            self.dir +=1
            self.face = 3
            self.spriteNum = 1
    
    def exit(self):
        print("EXIT MOV")
        pass

    def do(self):
        self.frame = (self.frame+1)%self.spriteNum
        self.x += self.dir
        self.x = clamp(0,self.x,1270)
        

    def draw(self):
        self.image.clip_draw(self.frame*80,100*self.face,80,100,self.x,self.y,80,100)

class DASH:
    def enter(self,event):
        print("dash")
        if event  ==  Shift_d:
            if self.face == 4:
                self.dir += 4
            if self.face == 3:
                self.dir -= 4
    
        elif event  ==  Shift_u:
            if self.face == 4:
                self.dir -= 4
            if self.face == 3:
                self.dir += 4

    def exit(self):
        print("exit dash")
        pass

    def do(self):
        self.frame = (self.frame+1)%self.spriteNum
        self.x += self.dir
        self.x = clamp(0,self.x,1270)
    
    def draw(self):
        self.image.clip_draw(self.frame*80,100*self.face,80,100,self.x,self.y,80,100)


next_state = {
    IDLE: {RD:MOVING,LD:MOVING,RU:MOVING,LU:MOVING,Shift_d:DASH},
    MOVING: {RD:IDLE,LD:IDLE,RU:IDLE,LU:IDLE,Shift_d:DASH},
    DASH :{RD:MOVING,LD:MOVING,RU:MOVING,LU:MOVING}
    # JUMP: {RD:MOVING,LD:MOVING,RU:MOVING,LU:MOVING}
}


class Knight:
    def __init__(self):
        self.x,self.y = 10,120
        self.frame = 0
        self.dir = 1 
        self.face = 1
        self.spriteNum = 1
        self.image = load_image('resource\\character_image_sprites\\knight_resource2.png')
    
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            try:
                self.cur_state = next_state [self.cur_state][event]
            except KeyError:
                 print(f'ERROR:State {self.cur_state.__name__} Event {event_name[event]}')

            self.cur_state.enter(self,event)
            


    def draw(self):
        self.cur_state.draw(self)
        

    def add_event(self,event):
        self.event_que.insert(0,event)

    def handle_event(self,event):
        if (event.type,event.key) in key_event_table:
            key_event = key_event_table[(event.type,event.key)]
            self.add_event(key_event)

