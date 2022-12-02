from pico2d import *
import loby_state
import arena_state

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
        if loby_state.coliBox | arena_state.coliBox:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0 , 0, 1270-1, 100
    def handle_collision(self, other, group):
        pass

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
        if loby_state.coliBox:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0 , 0, 1270-1, 100
    def handle_collision(self, other, group):
        pass

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
        if loby_state.coliBox:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0 , 0, 1270-1, 100

    def handle_collision(self, other, group):
        pass