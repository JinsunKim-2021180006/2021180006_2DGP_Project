#############################################
from pico2d import *
import game_framework
import random

import loby_state
import arenaOn_state

FRY  = range(1)
event_name = ['FRY']

PIXEL_PER_METER = (10.0 / 0.4) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9

GRAVITY_MPS = 9.8
GRAVITY_PPS = (GRAVITY_MPS * PIXEL_PER_METER)


class FLYING:
    
    def enter(self, event):
        print('ENTER JUMP')

        if self.x>1270:
            self.x = 1270
            self.dir = -1
        elif self.x<0:
            self.x = 0
            self.dir = 1
            
        if self.y>720:
            self.y = 720
            self.dir_y =-1
        elif self.y<110:
            self.y = 110
            self.dir = 1

                
    def exit(self, event):
        print('EXIT JUMP')



    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 8
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dir_y * GRAVITY_PPS * game_framework.frame_time
        pass

    def draw(self):
        self.image.clip_draw(int(self.frame)*500,600*self.dir,500,600,self.x,self.y,100,120)

next_state = {

    FLYING: {FRY:FLYING}
}


class Enemy2:
    def __init__(self):
        self.x,self.y = random.randint(100,1190),random.randint(120,620)
        self.frame = 0
        self.dir = 1
        self.dir_y = 1
        self.face_dir = 0
        self.image = load_image('resource\\character_image_sprites\\enemy2_resource.png')
        
        self.event_que = []
        self.cur_state = FLYING
        self.cur_state.enter(self, None)


    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)
        delay(0.01)

    def draw(self):
        self.cur_state.draw(self)
        if loby_state.coliBox | arenaOn_state.coliBox:
            draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def handle_collision(self, other, group):
        if group == 'enemy2:ground':
            self.dir = -self.dir
        pass
