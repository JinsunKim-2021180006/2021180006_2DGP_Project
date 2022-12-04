import pico2d
import game_framework

import intro_state
import start_state
import loby_state
import arena_state

state = [
    intro_state,
    start_state,
    loby_state,
    arena_state
    ]

 
pico2d.open_canvas(1270,720)
game_framework.run(state[3])
pico2d.close_canvas()



# class ATTACK:
        
#     def enter(self, event):
#         print('ENTER ATK')
#         self.atk_timer = 0.0
        
       
#     def exit(self, event):
#         print('EXIT ATK')


#     def do(self):
#         self.atk_timer += game_framework.frame_time
#         self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *game_framework.frame_time) % 7
#         pass

#     def draw(self):
#         if self.face_dir == 1:dma
#             self.image.clip_composite_draw(int(self.frame)*80,100*2,80,100,0,'',self.x,self.y,80,100)
#         else:
#             self.image.clip_composite_draw(int(self.frame)*80,100*2,80,100,0,'h',self.x,self.y,80,100)

        