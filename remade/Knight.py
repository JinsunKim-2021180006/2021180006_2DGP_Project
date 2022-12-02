from pico2d import *
import game_framework
import game_world
import arena_state
import GUI

RD, LD, RU, LU, ATK, ATK_U,\
DASH, SHOOT= range(8)

event_name = ['RD', 'LD', 'RU', 'LU', 'ATK', 'SHOOT']

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
    
    (SDL_KEYDOWN,SDLK_x) : ATK,
    (SDL_KEYUP,SDLK_x) : ATK_U,

    (SDL_KEYDOWN, SDLK_z): SHOOT

}


#2 : 상태의 정의
class IDLE:
    @staticmethod
    def enter(self,event):
        print('ENTER IDLE')
        self.dir = 0
        self.dir_y = -1

    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
        if event == SHOOT:
            self.Shoot_()


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
        if event == SHOOT:
            self.Shoot_()


    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 9
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 1270)


    def draw(self):
        if self.dir == -1:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'h',self.x,self.y,80,100)
        elif self.dir == 1:
            self.image.clip_composite_draw(int(self.frame)*80,100*4,80,100,0,'',self.x,self.y,80,100)


class ATTACK:
        
    def enter(self, event):
        print('ENTER ATK')
        self.atk_timer = 0.0
        
       
    def exit(self, event):
        print('EXIT ATK')


    def do(self):
        self.atk_timer += game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 7
        pass

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame)*80,100*2,80,100,0,'',self.x,self.y,80,100)
        else:
            self.image.clip_composite_draw(int(self.frame)*80,100*2,80,100,0,'h',self.x,self.y,80,100)

        


next_state = {
    IDLE:  {RU: MOVING,  LU: MOVING,  RD: MOVING,  LD: MOVING, ATK:ATTACK},
    MOVING:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, ATK:ATTACK},
    ATTACK: {RU: MOVING,  LU: MOVING,  RD: MOVING,  LD: MOVING, ATK:ATTACK, ATK_U:IDLE}
}


class Knight:

    def __init__(self):
        self.x, self.y = 100, 120
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.dir_y = -1

        self.HP = 5
        self.atk_timer = 0.0

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
                print(f'ERROR')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        if arena_state.coliBox:
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
        if group == 'knight:enemy':
            print("damage")
            self.HP -=1
        pass

    def GUI(self):
        HP_list = [25,60,95,130,165]

        for i in range(self.HP):
            hp = [GUI.HP(HP_list[i],680)]
            game_world.add_objs(hp, 1)
    
    def Shoot_(self):
        print("shoot")
        spirit = GUI.Shoot(self.x,self.y,self.face_dir*12)
        game_world.add_obj(spirit,1)
