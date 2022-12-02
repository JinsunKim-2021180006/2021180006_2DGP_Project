from pico2d import *
import arena_state

class Block:
    image = None
    
    def __init__(self,x,y):
        if Block.image == None:
            self.image = load_image('resource\\GUI_image\\platform.png')
        self.x,self.y = x, y
        
    def update(self):
        pass
        
    def draw(self):
        self.image.clip_draw(0,0,345,120,self.x,self.y,138,48)
        if arena_state.coliBox:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x -65, self.y-25, self.x+65, self.y+25

    def handle_collision(self, other, group):
        pass


class Wall:
    image = None

    def __init__(self,x,y):
        if Wall.image == None:
            self.image = load_image('resource\\GUI_image\\wall.png')
        self.x,self.y = x,y
    def update(self):
        if self.y >= 600:
            self.y -= 4
        pass
        
    def draw(self):
        self.image.clip_draw(0,0,120,1200,self.x,self.y,60,1000)
        if arena_state.coliBox:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x -25, self.y-600, self.x+25, self.y+600

    def handle_collision(self, other, group):
        pass
    