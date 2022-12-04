import random
from pico2d import *
import game_framework
import arena_state

PIXEL_PER_METER = (10.0 / 0.4) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9


import random
from pico2d import *
import game_framework
import arena_state

PIXEL_PER_METER = (10.0 / 0.4) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9

# 공벌래
class Enemy1:
    image = None
    def __init__(self):
        self.frame = 0
        self.dir = 1

        self.colli = False
        if Enemy1.image == None:
            Enemy1.image = load_image('resource\\character_image_sprites\\enemy1_resource.png')
        self.x, self.y = random.randint(100,1190),120
        
    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(int(self.frame)*610,500*5,500,500,self.x,120,70,70)
        else:
            self.image.clip_draw(int(self.frame)*610,500*1,500,500,self.x,120,70,70)

        if arena_state.coliBox:
            draw_rectangle(*self.get_bb())

    def update(self):        

        if self.x>1270:
            self.dir = -1
        elif self.x<0:
            self.dir = 1
        elif self.colli:
            self.colli = False
            self.dir = -self.dir


        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 3
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def handle_collision(self, other, group):
        if group == 'knight:enemy':
            self.colli = True
            pass
        pass



#붕붕 파리
class Enemy2:
    image = None
    def __init__(self):
        self.frame = 0

        self.dir = 1
        self.dir_y = 1
        
        self.colli = False
        if Enemy2.image == None:
            Enemy2.image = load_image('resource\\character_image_sprites\\enemy2_resource.png')
        self.x, self.y = random.randint(100,1190),random.randint(120,620)
        

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(int(self.frame)*500,600*3,500,600,self.x,self.y,100,120)
        else:
            self.image.clip_draw(int(self.frame)*500,600*1,500,600,self.x,self.y,100,120)

        if arena_state.coliBox:
            draw_rectangle(*self.get_bb())

    def update(self):
        
        if self.x>1270:
            self.x = 1270
            self.dir = -1
        if self.x<0:
            self.x = 0
            self.dir = 1    
        if self.y>720:
            self.y = 720
            self.dir_y =-1
        if self.y<110:
            self.y = 110
            self.dir_y = 1
        
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 8
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dir_y * RUN_SPEED_PPS * game_framework.frame_time

    def get_bb(self):
        return self.x - 35, self.y - 35, self.x + 35, self.y + 35

    def handle_collision(self, other, group):
        pass