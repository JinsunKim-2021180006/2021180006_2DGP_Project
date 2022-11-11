#############################################

from pico2d import *
import game_framework

RD, LD, RU, LU, SHIFT, SHIFT_U = range(6)

event_name = ['RD', 'LD', 'RU', 'LU', 'SHIFT', 'SHIFT_U']

PIXEL_PER_METER = (10.0 / 0.4) # 10 pixel 30 cm
RUN_SPEED_KMPH = 25.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,

    (SDL_KEYDOWN,SDLK_LSHIFT): SHIFT,
    (SDL_KEYUP,SDLK_LSHIFT): SHIFT_U
}


#2 : 상태의 정의
class IDLE:
    @staticmethod
    def enter(self,event):
        print('ENTER IDLE')
        self.dir = 0

    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')


    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 1


    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'',self.x,self.y,80,100)
        else:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'h',self.x,self.y,80,100)


class MOVING:

    def enter(self, event):
        print('ENTER RUN')
        global speed

        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

                
    def exit(self, event):
        print('EXIT RUN')
        self.face_dir = self.dir


    def do(self):
        # print(f'{self.speed*self.dir*game_framework.frame_time}')
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 9
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 1270)

    def draw(self):
        if self.dir == -1:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'h',self.x,self.y,80,100)
        elif self.dir == 1:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'',self.x,self.y,80,100)


next_state = {
    IDLE:  {RU: MOVING,  LU: MOVING,  RD: MOVING,  LD: MOVING, SHIFT:MOVING,SHIFT_U:MOVING},
    MOVING:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, SHIFT: IDLE,SHIFT_U: IDLE}
}


class Knight:

    def __init__(self):
        self.x, self.y = 20, 120
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('resource\\character_image_sprites\\knight_resource2.png')

        self.event_que = []
        self.cur_state = IDLE
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

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb(self):
        return self.x - 20, self.y - 25, self.x + 20, self.y + 50

    def handle_collision(self, other, group):
        print(' ')

