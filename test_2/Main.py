import pico2d
import game_framework

import intro_state
import start_state
import play_state

state = [
    intro_state,
    start_state,
    play_state
    ]


pico2d.open_canvas(1270,720)
game_framework.run(state[2 ])
pico2d.close_canvas()