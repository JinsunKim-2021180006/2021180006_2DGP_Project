from pico2d import *

class Hall:
    image = None
    
    def __init__(self,x,y):
        if Hall.image == None:
            self.image = load_image('resource\\background_image_sprites\\Colosseum_Passage_Back.png')
        self.x,self.y = x,y
    def update(self):
        pass
    
    def draw(self):
        self.image.draw(self.x//2,self.y//2)
        