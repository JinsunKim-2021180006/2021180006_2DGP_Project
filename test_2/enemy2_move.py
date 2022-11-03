from pico2d import *
import random

class IDLE:
    @staticmethod
    def enter(self,event):
        self.dir = 0

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame+1)%self.spriteNum
        pass
    
    @staticmethod
    def draw(self):
        self.image.clip_draw(self.frame*500,600*self.face,500,600,self.x,self.y,100,120)



class Flying:
    def enter(self):
        print("ENTER ANMY_2 FLYING")

    def exit(self):
        print("EXIT ANMY_2 FLYING")
    
    def do(self):
        self.frame = (self.frame + 1)%self.spriteNum
        self.x += self.dir
        self.y += self.dir
        self.x = clamp(0,self.x,1270)
        self.y = clamp(110,self.y,720)

    def draw(self):
        self.image.clip_draw(self.frame*500,600*self.fase,500,600,self.x,self.y,100,120)



class Enemy2:
    def __init__(self):
        self.x,self.y = random.randint(100,1190),random.randint(120,620)
        self.frame = 0
        self.dir = 1
        self.face = 3
        self.spriteNum = 1
        self.image = load_image('resource\\character_image_sprites\\enemy2_resource.png')
    
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)
        
        # if self.x>1270:
        #     self.dir = 3
        #     self.x = 1270
        #     move_X = -move_X
        # elif self.x<0:
        #     self.dir = 1
        #     self.x = 0  
        #     move_X = -move_X
            
        # if self.y>720:
        #     self.y = 720
        #     move_Y = -move_Y
        # elif self.y<110:
        #     self.y = 110
        #     move_Y = -move_Y
        # self.x += move_X
        # self.y += move_Y

    def draw(self):
        self.cur_state.draw(self)
    
