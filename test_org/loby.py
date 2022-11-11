#로비
from pico2d import *

class Loby:
    image = None
    
    def __init__(self,x,y):
        if Loby.image == None:
            self.image = load_image('resource\\background_image_sprites\\Colosseum_Lobby.png')
        self.x,self.y = x,y
    def update(self):
        pass
        
    def draw(self):
        self.image.draw(self.x//2,self.y//2)
        