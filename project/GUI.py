from pico2d import *
import play_state
import game_world
import game_framework


class HP:
    image = None
    
    def __init__(self,x,y):
        if HP.image == None:
            self.image = load_image('resource\\GUI_image\\HP_mask.png')
            self.x,self.y = x, y
   
    def update(self):
        pass

    def handle_collision(self, other, group):
        if group == 'knight:enemy':
            game_world.remove_obj(self)
           
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
        

class SHOOT:
    image = None

    def __init__(self,x,y,velo):
        if MP.image == None:
            self.image = load_image('resource\\character_image_sprites\\Spirit_Icon.png')
            self.x,self.y = x, y
            self.velo = velo
   
    def draw(self):
        if play_state.coliBox:
            draw_rectangle(*self.get_bb())
        
        if self.velo <=0:
            self.image.clip_composite_draw(0,0,115,72,0,'',self.x,self.y,110,67)
        else:
            self.image.clip_composite_draw(0,0,115,72,0,'h',self.x,self.y,110,67)
    

    def update(self):
        self.x += self.velo
        if self.x<10 or self.x>1270-10:
            game_world.remove_obj(self)
        pass

    def handle_collision(self,other,group):
        if group == 'spirit:enemy':
            print('hit')
            game_world.remove_obj(self)
        pass


    def get_bb(self):
        return self.x - 50, self.y - 30, self.x + 50, self.y + 30

class ATTACK_WING:
    image = None

    def __init__(self,x,y,velo):
        self.timer = 0
        if MP.image == None:
            self.image = load_image('resource\\character_image_sprites\\Attack_Icon.png')
            self.x,self.y = x, y
            self.velo = velo

    def draw(self):
        if play_state.coliBox:
            draw_rectangle(*self.get_bb())
        
        if self.velo <=0:
            self.image.clip_composite_draw(0,0,127,277,0,'h',self.x-40,self.y,42,92)
        else:
            self.image.clip_composite_draw(0,0,127,277,0,'',self.x+40,self.y,42,92)
    

    def update(self):
        self.timer += 0.5

        if self.timer == 10:
            game_world.remove_obj(self)
        pass

    def handle_collision(self,other,group):
        pass
    
    def get_bb(self):
        return self.x, self.y, self.x, self.y


class Door:
    image = None
    def __init__(self,x,y,locCHk): #0=up 1=updown 2=down
        if self.image == None:
            if locCHk == 0:
                self.image = load_image('resource\\GUI_image\\Door_up.png')
                self.x,self.y = x, y
            if locCHk == 1:
                self.image = load_image('resource\\GUI_image\\Door_up.png')
                self.x,self.y = x, y
            if locCHk == 2:
                self.image = load_image('resource\\GUI_image\\Door_down.png')
                self.x,self.y = x, y
    
    def draw(self):
        self.image.draw(self.x,self.y,215/2.5,250/2.5)
        if play_state.coliBox:
            draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 35, self.y - 35, self.x + 35, self.y + 35

    def handle_collision(self, other, group):
        pass
