from pico2d import *
import arenaOn_state

class Arena:
    image = None
    
    def __init__(self,x,y):
        if Arena.image == None:
            self.image = load_image('resource\\background_image_sprites\\Colosseum_Arena.png')
        self.x,self.y = x,y
    def update(self):
        pass
    
    def draw(self):
        self.image.draw(self.x//2,self.y//2)
        if arenaOn_state.coliBox:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0 , 0, 1270-1, 100
    def handle_collision(self, other, group):
        pass