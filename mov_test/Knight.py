from pico2d import *
import game_framework
import game_world
import arenaOn_state

RD, LD, RU, LU,\
SPACE, FALL,\
LAND_I, LAND_M= range(8)

event_name = ['RD', 'LD', 'RU', 'LU', 'SPACE', 'FALL', 'LAND_I', 'LAND_M']

PIXEL_PER_METER = (10.0 / 0.4) # 10 pixel 30 cm
RUN_SPEED_KMPH = 25.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9

GRAVITY_MPS = 9.8
GRAVITY_PPS = (GRAVITY_MPS * PIXEL_PER_METER)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,

    (SDL_KEYDOWN,SDLK_SPACE):SPACE
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
        if events == SPACE:
            self.air_mov = False


    @staticmethod
    def do(self):
        if not self.colli:
            self.add_event(FALL)

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'',self.x,self.y,80,100)
        else:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'h',self.x,self.y,80,100)


class MOVING:

    def enter(self, event):
        self.dir = 0
        print('ENTER RUN')
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
        self.dir = 0

        if event == SPACE:
            self.air_move = True

    def do(self):
        # print(f'{self.speed*self.dir*game_framework.frame_time}')
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 9
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dir_y * GRAVITY_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 1270)
        self.y = clamp(120,self.y,150)

    def draw(self):
        if self.dir == -1:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'h',self.x,self.y,80,100)
        elif self.dir == 1:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'',self.x,self.y,80,100)


class JUMP:
    
    def enter(self, event):
        print('ENTER JUMP')
        self.dir = 0
        if self.jumping == False:
            self.jumping = True
            if event == SPACE:
                self.dir_y += 2
            
                
    def exit(self, event):
        print('EXIT JUMP')
        self.dir = 0


    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 9
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dir_y * GRAVITY_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 1270)
        

        if self.y == jump:
            self.jumping= True

        jump = self.y+80
        pass

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'',self.x,self.y,80,100)
        else:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'h',self.x,self.y,80,100)


class FALLING:
    
    def enter(self, event):
        print('ENTER JUMP')
                
    def exit(self, event):
        print('EXIT JUMP')


    def do(self):
        pass

    def draw(self):
        pass


    
next_state = {
    IDLE:  {RU: MOVING,  LU: MOVING,  RD: MOVING,  LD: MOVING, SPACE:JUMP,FALL:FALLING},
    MOVING:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, SPACE:JUMP, FALL:FALLING},
    JUMP : {RU: MOVING,  LU: MOVING,  RD: MOVING,  LD: MOVING, SPACE:JUMP, FALL:FALLING},
    FALLING: {RU: FALLING,  LU: FALLING,  RD: FALLING,  LD: FALLING, SPACE:FALLING, FALL:IDLE, 
                LAND_I: IDLE, LAND_M: MOVING}
}


class Knight:

    def __init__(self):
        self.x, self.y = 100, 120
        self.frame = 0
        self.dir, self.face_dir = 0, 1

        self.vel = 0
        self.colli = True #바닥에 닿았는지 확인

        self.air_mov =False
        self.timer = 0
        self.jump_y = 0.0

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
        if  arenaOn_state.coliBox:
            draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 50

    def handle_collision(self, other, group):
        if group == 'knight:ground':
            self.colli = False
