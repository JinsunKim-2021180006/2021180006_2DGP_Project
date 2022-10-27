from pico2d import *

frame = 0
spriteNum = 1

class Knight:
    def __init__(self,x,y):
        self.x,self.y = x, y
        self.frame = 0
        self.dir = 1
        self.image = load_image('resource\\character_image_sprites\\knight_resource2.png')
    
    def update(self,DirX,DirY):
        global state_chk

        self.frame = (self.frame+1) % spriteNum
        self.x += DirX*5
        self.y += DirY*5

        if self.x >= 1270:
            self.x = 1270
        elif self.x <= 0:
            self.x = 0


        delay(0.01)

    def draw(self):
        self.image.clip_draw(self.frame*80,100*self.dir,80,100,self.x,self.y,80,100)