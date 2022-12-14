import random
from pico2d import *
import game_framework
import game_world
import play_state
import Knight

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
    def __init__(self,y):
        self.frame = 0
        self.dir = 1
        self.hp = 3

        self.colli = False
        if Enemy1.image == None:
            Enemy1.image = load_image('resource\\character_image_sprites\\enemy1_resource.png')
        self.x, self.y = random.randint(100,1190),y
        
    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(int(self.frame)*610,500*5,500,500,self.x,self.y,70,70)
        else:
            self.image.clip_draw(int(self.frame)*610,500*1,500,500,self.x,self.y,70,70)

        if play_state.coliBox:
            draw_rectangle(*self.get_bb())

    def update(self):        

        if self.x>1270:
            self.dir = -1
        elif self.x<0:
            self.dir = 1
        elif self.colli:
            self.colli = False
            self.dir = -self.dir

        if self.hp == 0:
            game_world.remove_obj(self)

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 3
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def handle_collision(self, other, group):
        if group == 'knight:enemy':
            self.colli = True
            if not Knight.atkCHK:
                play_state.enemy_cnt -= 1
                game_world.remove_obj(self)
            



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

        if play_state.coliBox:
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
        if group == 'knight:enemy':
            if not Knight.atkCHK:
                play_state.enemy_cnt -= 1
                game_world.remove_obj(self)
            
        pass


class Boss:
    image = None
    def __init__(self):
        self.frame = 0

        self.dir = 1
        self.dir_y = 1
        
        self.colli = False
        if self.image == None:
            self.image = load_image('resource\\character_image_sprites\\Boss1_resource.png')
        self.x, self.y = 750,500
        

    def draw(self):
        if self.dir == -1:
            self.image.clip_composite_draw(int(self.frame)*500,500*7,500,500,0,'h',self.x,self.y,80,100)
        else:
            self.image.clip_composite_draw(int(self.frame)*500,500*7,500,500,0,'',self.x,self.y,80,100)


        if play_state.coliBox:
            draw_rectangle(*self.get_bb())

    def update(self):
        
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 7


    def get_bb(self):
        return self.x - 35, self.y - 35, self.x + 35, self.y + 35

    def handle_collision(self, other, group):
        pass