from pico2d import *
import game_framework

RD,LD,RU,LU = range(4)

event_name = ['RD', 'LD', 'RU', 'LU']


PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU
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
        self.face_dir = self.dir
        pass

    def do(self):
        self.frame = (self.frame+1)%self.spriteNum
        self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0,self.x,1270)
        

    def draw(self):
        self.image.clip_draw(self.frame*80,100*self.face,80,100,self.x,self.y,80,100)



next_state = {
    IDLE: {RD:MOVING,LD:MOVING,RU:MOVING,LU:MOVING},
    MOVING: {RD:IDLE,LD:IDLE,RU:IDLE,LU:IDLE}
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
        draw_rectangle(*self.get_bb())
        

    def add_event(self,event):
        self.event_que.insert(0,event)

    def handle_event(self,event):
        if (event.type,event.key) in key_event_table:
            key_event = key_event_table[(event.type,event.key)]
            self.add_event(key_event)

    def get_bb(self):
        return self.x -20, self.y -25, self.x +20, self.y +45

    def handle_collision(self, other, group):
        pass

