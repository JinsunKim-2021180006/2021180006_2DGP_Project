from pico2d import *
import game_framework
import random

frame = 0
spriteNum = 1
move_X, move_Y = 3,2
enemy2_num = 1


class Enemy2:
    def __init__(self):
        self.x,self.y = random.randint(100,1190),random.randint(120,620)
        self.frame = 0
        self.dir = 3
        self.image = load_image('resource\\character_image_sprites\\enemy2_resource.png')
    
    def update(self):
        global move_X,move_Y,enemy2_num
        self.frame = (self.frame+1) % spriteNum
        
        if self.x>1270:
            self.dir = 3
            self.x = 1270
            move_X = -move_X
        elif self.x<0:
            self.dir = 1
            self.x = 0  
            move_X = -move_X
            
        if self.y>720:
            self.y = 720
            move_Y = -move_Y
        elif self.y<110:
            self.y = 110
            move_Y = -move_Y
        self.x += move_X
        self.y += move_Y
           

      
        delay(0.01)

    def draw(self):
        self.image.clip_draw(self.frame*500,600*self.dir,500,600,self.x,self.y,100,120)
