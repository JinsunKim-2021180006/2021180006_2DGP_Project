from pico2d import *
import arena_state
import game_world

class HP:
    image = None
    
    def __init__(self,x,y):
        if HP.image == None:
            self.image = load_image('resource\\GUI_image\\HP_mask.png')
            self.x,self.y = x, y
   
    def update(self):
        
        pass
    
    def draw(self):
        self.image.draw(self.x,self.y)

class MP:
    image = None
    
    def __init__(self,x,y):
        if MP.image == None:
            self.image = load_image('resource\\GUI_image\\Lifeblood_mask.png')
            self.x,self.y = x, y
   
    def update(self):
        pass
    
    def draw(self):
        self.image.draw(self.x,self.y)
        

class Shoot:
    image = None

    def __init__(self,x,y,velo):
        if MP.image == None:
            self.image = load_image('resource\\character_image_sprites\\Spirit_Icon.png')
            self.x,self.y = x, y
            self.velo = velo
   
    def update(self):
        self.x+= self.velo
        if self.x<10 or self.x>1270-10:
            game_world.remove_obj(self)       
        pass

    def get_bb(self):
        return self.x - 50, self.y - 30, self.x + 50, self.y + 30

    def draw(self):
        if arena_state.coliBox:
            draw_rectangle(*self.get_bb())
        
        if self.velo <=0:
            self.image.clip_composite_draw(0,0,115,72,0,'',self.x,self.y,110,67)
        else:
            self.image.clip_composite_draw(0,0,115,72,0,'h',self.x,self.y,110,67)
    
