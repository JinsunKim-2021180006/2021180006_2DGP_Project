from pico2d import *
import game_framework
import game_world
import arena_state
import loby_state
import GUI

RD, LD, RU, LU, ATK, ATK_U,\
SHOOT_KEY= range(7)

event_name = ['RD', 'LD', 'RU', 'LU', 'ATK', 'atk_u','SHOOT']

PIXEL_PER_METER = (10.0 / 0.4) # 10 pixel 30 cm
RUN_SPEED_KMPH = 25.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9

shoot_sound = None

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    
    (SDL_KEYDOWN,SDLK_x) : ATK,
    (SDL_KEYUP,SDLK_x) : ATK_U,

    (SDL_KEYDOWN, SDLK_z): SHOOT_KEY

}

class IDLE:
    @staticmethod
    def enter(self,event):
        self.atkChk = False
        self.anmiCnt = 1
        self.dir = 0
 
    @staticmethod
    def exit(self, event):
        if event == SHOOT_KEY:
            self.Shoot()
        if event == ATK:
            self.atkChk = True
            self.atk_range = 30
            self.frameNum = 2
            self.anmiCnt = 7
            self.Attack()
        if event ==ATK_U:
            self.atkChk = False
            self.atk_range = 0
            self.anmiCnt = 1
            self.frameNum = 4

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % self.anmiCnt

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame)*80,100*self.frameNum,80,100,0,'',self.x,self.y,80,100)
        else:
            self.image.clip_composite_draw(int(self.frame)*80,100*self.frameNum,80,100,0,'h',self.x,self.y,80,100)

class MOVING:

    def enter(self, event):
        self.anmiCnt = 9
        self.frameNum = 4
        self.atkChk = False
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

    def exit(self, event):
        self.face_dir = self.dir
        if event == SHOOT_KEY:
            self.Shoot()
        
        if event == ATK:
            self.atkChk = True
            self.atk_range = 30
            self.anmiCnt = 7
            self.frameNum = 2
            self.Attack()
        if event ==ATK_U:
            self.atkChk = False
            self.atk_range = 0
            self.anmiCnt = 9
            self.frameNum = 4

    def do(self):
        global shoot_sound

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % self.anmiCnt
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 1270)


    def draw(self):
        if self.dir == -1:
            self.image.clip_composite_draw(int(self.frame)*80,100*self.frameNum,80,100,0,'h',self.x,self.y,80,100)
        elif self.dir == 1:
            self.image.clip_composite_draw(int(self.frame)*80,100*self.frameNum,80,100,0,'',self.x,self.y,80,100)


next_state = {
    IDLE:  {RU: MOVING,  LU: MOVING,  RD: MOVING,  LD: MOVING, ATK:IDLE, SHOOT_KEY:IDLE},
    MOVING:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, ATK:MOVING, SHOOT_KEY:MOVING},
}


class Knight:

    def __init__(self):
        global shoot_sound
        self.x, self.y = 100, 120
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.frameNum = 4
        self.anmiCnt = 1
        
        self.hp = None
        self.hp_cnt = 5
        self.mp = 3

        self.atkimg = None
        self.atk_range = 0
        self.atkChk = False

        self.spirit = []

        self.image = load_image('resource\\character_image_sprites\\knight_resource2.png')
        shoot_sound = load_wav('resource\\sound\\knight_shoot.wav')
        shoot_sound.set_volume(20)



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
        if arena_state.coliBox | loby_state.coliBox:
            draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    #=============================================================================
    #충돌체크 용
    def get_bb(self):
        if self.face_dir == 1:
            return self.x - 20, self.y - 30, self.x + self.atk_range + 20, self.y + 50
        elif self.face_dir == -1:
            return self.x - self.atk_range - 20, self.y - 30, self.x + 20, self.y + 50
            


    def handle_collision(self, other, group):
        if group == 'knight:enemy':
            pass
        pass
    #=============================================================================
    def Gui(self):
        HP_list = [30,65,100,135,170]
        for i in range(5):
            self.hp = [GUI.HP(HP_list[i],680)]
            game_world.add_objs(self.hp, 1)

        mp_list = [30,65,100]
        for j in range(self.mp):
            mp = [GUI.MP(mp_list[j],630)]
            game_world.add_objs(mp, 1)

    
    #=============================================================================
    # 공격 함수들
    def Shoot(self):
        
        self.spirit = GUI.SHOOT(self.x,self.y,self.face_dir*12)
        game_world.add_obj(self.spirit,1)
    
    def Attack(self):
        shoot_sound.play()
        self.atkimg = GUI.ATTACK_WING(self.x,self.y,self.face_dir*1)
        game_world.add_obj(self.atkimg,1)
        pass
