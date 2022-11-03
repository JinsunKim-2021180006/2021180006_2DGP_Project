from pico2d import *

class Arena:
    image = None
    def __init__(self):
        if Arena.image == None:
            image = load_image('resource\\background_image_sprites\\Colosseum_Arena.png')
        
        pass
   
    def update(self):
        pass

    def draw(self):
        self.image.draw(1270,720)