from pico2d import *
import arenaOn_state

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
        

