import pico2d
import game_framework

import play_state

state = [
    play_state
    ]


pico2d.open_canvas(1270,720)
game_framework.run(state[0])
pico2d.close_canvas()